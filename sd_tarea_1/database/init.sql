CREATE TABLE IF NOT EXISTS gauss_lru_2mb (
    id SERIAL PRIMARY KEY,          -- id autoincremental
    idx INT NOT NULL,               -- índice de la pregunta
    question TEXT NOT NULL,         -- la pregunta
    yahoo_answer TEXT NOT NULL,     -- respuesta de Yahoo
    gemini_answer TEXT,             -- respuesta de Gemini (puede ser NULL al inicio)
    score INT NOT NULL,             -- puntaje de la respuesta
    cache_hit INT DEFAULT 0,        -- numero de veces que el resultado se ha obtenido de la caché
    cache_miss INT DEFAULT 0,       -- numero de veces que el resultado no se ha obtenido de la caché
    creation_date TIMESTAMP DEFAULT NOW()  -- fecha de creación
);

CREATE TABLE IF NOT EXISTS gauss_lru_5mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,   
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gauss_lru_10mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,      
    cache_miss INT DEFAULT 0,  
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gauss_lfu_2mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,        
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gauss_lfu_5mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,        
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gauss_lfu_10mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,     
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS zipf_lru_2mb (
    id SERIAL PRIMARY KEY,         
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,     
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW() 
);

CREATE TABLE IF NOT EXISTS zipf_lru_5mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,   
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS zipf_lru_10mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,  
    cache_miss INT DEFAULT 0,      
    creation_date TIMESTAMP DEFAULT NOW()
);



CREATE TABLE IF NOT EXISTS zipf_lfu_2mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,   
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zipf_lfu_5mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,        
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zipf_lfu_10mb (
    id SERIAL PRIMARY KEY,          
    idx INT NOT NULL,               
    question TEXT NOT NULL,         
    yahoo_answer TEXT NOT NULL,     
    gemini_answer TEXT,             
    score INT NOT NULL,             
    cache_hit INT DEFAULT 0,      
    cache_miss INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT NOW()
);





CREATE OR REPLACE FUNCTION check_qa(
    table_name TEXT,
    p_idx INT
) RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    result_json JSON;
BEGIN
    -- Ejecuta la consulta para obtener los datos en formato JSON
    EXECUTE format('
        SELECT json_build_object(
            ''question'', question,
            ''yahoo_answer'', yahoo_answer,
            ''gemini_answer'', gemini_answer,
            ''score'', score
        ) 
        FROM %I 
        WHERE idx = $1', table_name)
    INTO result_json
    USING p_idx;

    IF result_json IS NOT NULL THEN
        RETURN result_json;
    ELSE
        RETURN NULL;

    END IF;
END;
$$;




CREATE OR REPLACE PROCEDURE register_cache_event(
    table_name TEXT,
    p_idx INT,
    event_type TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF event_type = 'hit' THEN
        EXECUTE format('UPDATE %I SET cache_hit = cache_hit + 1 WHERE idx = $1', table_name)
        USING p_idx;
    ELSIF event_type = 'miss' THEN
        EXECUTE format('UPDATE %I SET cache_miss = cache_miss + 1 WHERE idx = $1', table_name)
        USING p_idx;
    ELSE
        RAISE EXCEPTION 'Unknown event type: %', event_type;
    END IF;
END;
$$;



CREATE OR REPLACE PROCEDURE save_qa(
    table_name TEXT,
    p_idx INT,
    p_question TEXT,
    p_yahoo_answer TEXT,
    p_gemini_answer TEXT,
    p_score NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format(
        'INSERT INTO %I (idx, question, yahoo_answer, gemini_answer, score) VALUES ($1, $2, $3, $4, $5)',
        table_name
    )
    USING p_idx, p_question, p_yahoo_answer, p_gemini_answer, p_score;
END;
$$;

