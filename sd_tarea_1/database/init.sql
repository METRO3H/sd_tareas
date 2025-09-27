CREATE TABLE IF NOT EXISTS gauss_lru_5mb_1min  (
    id SERIAL PRIMARY KEY,          -- id autoincremental
    idx INT NOT NULL,               -- índice de la pregunta
    question TEXT NOT NULL,         -- la pregunta
    yahoo_answer TEXT NOT NULL,     -- respuesta de Yahoo
    gemini_answer TEXT,             -- respuesta de Gemini (puede ser NULL al inicio)
    score NUMERIC(5,2),             -- puntaje de la respuesta (decimal opcional)
    cache_hit INT DEFAULT 0,        -- numero de veces que el resultado se ha obtenido de la caché
    creation_date TIMESTAMP DEFAULT NOW()  -- fecha de creación
);




CREATE OR REPLACE FUNCTION check_qa(
    table_name TEXT,
    p_idx INT
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    row_exists BOOLEAN;
BEGIN
    -- Verifica si existe una fila con idx = p_idx
    EXECUTE format('SELECT EXISTS(SELECT 1 FROM %I WHERE idx = $1)', table_name)
    INTO row_exists
    USING p_idx;

    IF row_exists THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE; 
    END IF;
END;
$$;




CREATE OR REPLACE PROCEDURE register_cache_hit(
    table_name TEXT,
    p_idx INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('UPDATE %I SET cache_hit = cache_hit + 1 WHERE idx = $1', table_name)
    USING p_idx;
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
