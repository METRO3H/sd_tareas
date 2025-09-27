from sentence_transformers import SentenceTransformer, util

# Cargar un modelo de embeddings preentrenado
model = SentenceTransformer("all-MiniLM-L6-v2")

def score_answer(yahoo_answer, gemini_answer):
    
    # Convertir las respuestas en embeddings
    emb1 = model.encode(yahoo_answer, convert_to_tensor=True)
    emb2 = model.encode(gemini_answer, convert_to_tensor=True)

    # Calcular similitud de coseno
    score = util.cos_sim(emb1, emb2).item()

    score = round(score * 100)
    
    print(f"Yahoo answer vs Gemini answer: {score}")
    
    return score


    

if __name__ == "__main__":
    
    yahoo_answer = "No, philosophy is not a social science.  In college it is usually categorized as part of the Humanities and Arts section or department.  The difference between philosophy and social science is that philosophy is a belief system based on the use of reason and logic (Metaphysics), while the social sciences are a belief system based on empirical observation to find truth or SCIENCE.  Thus, a social science like sociology is based on the actual physical study of society to explain social phenomena, but a philosophy like ethics or existentialism is based on the the use of thought experiments and rational thinking to explain human behavior and society."
    
    gemini_answer = "That's a really fascinating and hotly debated question! The short answer is: **yes, philosophy is undeniably a form of social science, but it's a very specific and nuanced one.** It's often described as a 'social science of thought' rather than a traditional social science like sociology or psychology. Here's a breakdown of why and how: **Arguments for Philosophy as Social Science:** * **Focus on Human Behavior:** Philosophy investigates fundamental questions about human nature, morality, knowledge, and social structures – all of which are deeply intertwined with how we interact with each other and the world. * **Social Context:** Philosophical arguments are rarely made in a vacuum. They are always shaped by the historical, cultural, and political contexts in which they are debated.  Consider: * **Ethics:** Moral philosophy is profoundly influenced by societal norms, religious beliefs, and legal systems. * **Political Philosophy:**  Ideas about justice, rights, and governance are shaped by power dynamics, economic systems, and historical events. * **Epistemology:** How we know what we know is shaped by our social and cultural backgrounds – our education, language, and shared experiences. * **Social Inquiry:** Philosophy actively engages with social issues like inequality, discrimination, and social change. It analyzes the *causes* and *consequences* of these issues. * **Social Theory:**  Philosophers develop theories about how societies function, how social interactions occur, and how power is distributed. These theories are often informed by observations of social phenomena. * **Social Critique:**  Philosophy often critiques existing social norms and institutions, prompting reflection and potential reform. **How Philosophy Relates to Social Science:** * **Different Methodologies:**  Philosophy employs methods similar to those used in social science, including: * **Analysis:** Examining arguments, concepts, and assumptions. * **Logical Reasoning:**  Using deductive and inductive reasoning to build arguments. * **Conceptual Analysis:**  Clarifying and defining concepts. * **Historical Analysis:**  Examining the historical development of ideas. * **Critical Analysis:**  Evaluating the strengths and weaknesses of arguments and theories. * **Comparative Analysis:** Philosophers often compare and contrast different philosophical traditions and theories to understand the roots of social problems and potential solutions. * **Social Theory as a Tool:**  Philosophical theories (like Marxism, feminism, post-structuralism) are used as frameworks for analyzing social phenomena and developing social policies. **Key Differences from Traditional Social Sciences:** * **Emphasis on Reason:**  Social sciences often prioritize empirical observation and quantitative data. Philosophy, while valuing reason, relies heavily on conceptual analysis, logical argumentation, and critical reflection. * **Focus on Questions of Value:** Social sciences often deal with objective facts. Philosophy grapples with questions of value, meaning, and purpose – areas that are inherently subjective. **In conclusion:** Philosophy is a vital and increasingly recognized form of social science. It provides a critical lens for understanding the complexities of human society and the challenges of building a just and equitable world.  It’s not simply a detached academic exercise; it’s a deeply engaged and influential field that shapes our understanding of ourselves and our place in the world. --- **Resources for Further Exploration:** * **Stanford Encyclopedia of Philosophy:** [https://plato.stanford.edu/](https://plato.stanford.edu/) - A comprehensive resource for philosophical topics. * **Internet Encyclopedia of Philosophy:** [https://iep.utm.edu/](https://iep.utm.edu/) - Another excellent resource for philosophical information. To help me tailor my response further, could you tell me: *   What specifically about philosophy's connection to social science are you most interested in? (e.g., its methods, its role in understanding social problems, its influence on social theory?)"
    
    score_answer(yahoo_answer, gemini_answer)