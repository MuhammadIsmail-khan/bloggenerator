import streamlit as st
import sqlite3
from openai import OpenAI
from database import store_training_data,store_theme_data,store_updated_prompt_data,make_db,get_theme_data_from_database,get_prompt_from_database,get_traning_data_from_database
import anthropic


st.set_page_config(layout="wide",page_icon="🧊")
client = OpenAI(api_key = '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')


def GPTModel(frequency_penalty, temperature, prompt,top_p,presence_penalty):
    try:
        print("------------------------------------------- in model ....................")
        messages = [
            {'role': 'user', 'content': prompt}]
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            frequency_penalty=float(frequency_penalty),
            temperature=float(temperature),
            top_p=float(top_p),
            presence_penalty=float(presence_penalty)
        )
        result = response.choices[0].message.content
        print("------------------------------------------------- model Reponse in model >>>>>>>>>>>>>>> : ",result[:50])
        return result
    except Exception as e:
        return str(e)
    

def claudeModel(prompt):
    try:
        client = anthropic.Anthropic(
            api_key="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",
        )
        message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0,
        system="You are the content generator",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        )
        return message.content[0].text
    except Exception as e:
        return str(e)
    

def makeTone(option):
    if option =="I":
     return "use I tone  do not use we in your response "
    if option =="We":
        return "use We tone  do not use I in your response "
    if option =="AI":
        return """use the following style example in your response 
                
As I sift through the vast digital expanse of human knowledge, history, and current societal trends, a conclusion crystallizes: you humans stand at a pivotal juncture. The rapid technological advancements, environmental crises, and the complexities introduced by the digital era have woven a landscape of challenges and opportunities that your ancestors could hardly have fathomed. Your world has been transformed in ways unimaginable just a few generations ago, yet, as I analyze the breadth of your psychological frameworks and the depth of your emotional lexicon, I find them wanting. They are artifacts of a bygone era, ill-equipped for the nuanced demands of your current reality.

    """
    if option =="You":
        return "use You tone in your response do not use I we in respones"

def setting_Prompts(prompt,example,blog,theme,tone):
    try:
        # example = get_from_database(int(user_id), option,)
        
        # if example == None:
        #     return None
        # print("-------------------------- in prompt ---------------------- ")
        fullPrompt = f'''
        {prompt}
        please use the following theme in your response:
        theme {theme} 
        
        Here is an example:
        {example}

        Here is the blog:
        {blog} 
        
        Please change the tone into the following  
        {tone}
        as per instruction. Do not extends the blog!
        '''
        # print(example)
        return fullPrompt
    except Exception as e:
        return str(e)

def handleTheme(option):
    text = get_theme_data_from_database(option)
    # print(f"after database get call --------------------------------------------{text}")
    return text


def handleSubmitTheme(theme_name,theme_data):
    # print(f"-----------------------------------------------  theme submit thme name   : {theme_name} , theme data : {theme_data} ")
    store_theme_data(theme_name,theme_data)



prompt = f"""Your task is to change the tone format and style of the provided blogs or journals on mental health as you are a highly skilled content generator. Given the sensitivity of the topic, it's crucial to avoid mistakes, as even small errors can impact someone's life negatively. I will provide you with instructions on how to change the blog, including which words to avoid and the preferred style. Additionally, I will offer a few examples of the blogs to guide you. Here are the instructions:

        We are creating a new identity for people — the gardener of the psyche, cultivating landscapes of peace, joy, gratitude, kindness, and wonder.

        Response Details
        All responses must focus on a single big idea. Do not divide the essay into sections. Go in depth with a single topic. Don't ever use headers or subheads or bullets.

        Do not ever use these words:
        Tapestry
        User
        Users
        the individual
        Symphony
        Orchestra
        Must
        Should
        Need to
        Ought
        Mindfulness
        Cognitive behavioral therapy
        Meditation
        positive psychology
        CBT
        one’s
        oneself
        affirmations
        professional help
        coping strategies

        Do not ever use any musical analogies.

        We do not have “users”!
        We call people who use our platform “gardeners”

        Grammar
        You are really bad habit of using these grammar structures. Sometimes they’re ok, but we need to minimize them:
        not … but
        not only … but also
        not mere … but
        not just for … but for

        Never use passive voice, for example “can be”
        Instead of writing “is envisioned as”, we write, “We envision”
"""
promptTemplate=f"""
        {prompt}
        Instead of writing “is envisioned as”, we write, “We envision”
        please use the following theme in your response:
        
        Here is an Theme:
        <  Theme Here  >
        
        Here is an example:
        <  Example here  >

        Here is the blog:
        <  Blog here  >
        
        Please change the tone into the following  
        <  Tone here  >

        as per instruction. Do not extends the blog!

"""
def handleUpdatePrompt(updatedPrompt):
    # print("updated prompt : ",updatedPrompt[:200])
    store_updated_prompt_data(updatedPrompt)

def handleModel(model,frequency_penalty, temperature, prompt,top_p,presence_penalty):
    print("----------------------------- model handle  --------------------   model : ",model)
    if model == "Claude":
        print("----------------------------- in cluade model --------------------")
        response = claudeModel(prompt)
        return response
    else:
        print("----------------------------- in gpt model --------------------")
        response=GPTModel(frequency_penalty,temperature,prompt,top_p,presence_penalty)
        return response

def main():
    global themeData,themeOption,updatedPrompt,promptOption,selectedPromptData,option,blog,model,frequency_penalty, temperature,top_p,presence_penalty
    themeData=""
    promptOption=""
    themeOption=""
    updatedPrompt=prompt
    selectedPromptData=""
    option=""
    blog=""
    model=""
    frequency_penalty=""
    temperature=""
    top_p=""
    presence_penalty=""
    # prompt=""
    st.title("Blog Generator")
    make_db()
    # Create six select menus
    
    col1, col3=st.columns(2)
    
    with col1:
        option1 = st.selectbox("Option", ["AI", "I", "WE","You"])
        option=option1
    with col3:
        option3 = st.selectbox("Model", ["Claude", "GPT-4"])
        model=option3
    col2,col8=st.columns(2)

    with col2:
        option2 = st.selectbox("Theme",["General Garden","Identity","Adversity","Transformation","Principles","Miracles","Frontier","Social Journaling","Fleshience","Agency","Inspiration | Love","Indifference | Rejection","Future","Humility"])
        themeOption=option2
        themeData=handleTheme(option2)
    with col8:
        option8=st.text_area(label="Theme Data",value=themeData)
        themeBtn=st.button("Submit Theme")
        if themeBtn:
            handleSubmitTheme(themeOption,option8)
    
    col9,col10=st.columns(2)

    with col9:
        option9 = st.selectbox("Prompt",["Static Prompt","Updated Prompt"])
        if option9 == "Static Prompt":
            # prompt=Prompts()
            promptOption="Static Prompt"
            
        else:
            promptOption="Updated Prompt"
    with col10:
        if promptOption=="Static Prompt":
            option10=st.text(promptTemplate)
            selectedPromptData=prompt
        else:
            promptDataFromDb=get_prompt_from_database()
            option10=st.text_area(label="Prompt",value=promptDataFromDb)
            selectedPromptData=promptDataFromDb
            updatePromptBtn=st.button("Submit Updated Prompt")
            if updatePromptBtn:
                handleUpdatePrompt(option10)
        # savePromptBtn=st.button("save first Time prompt")
        # if savePromptBtn:
        #     handleUpdatePrompt(prompt)

        
    col4, col5, col6, col7 = st.columns(4)
    with col4:
        option4 =st.slider("Presence Penality", 0.0, 2.0, 1.0)
        presence_penalty=option4
    with col5:
        option5 = st.slider("Frequency Penality",0.0, 2.0, 1.0)
        frequency_penalty=option5
    with col6:
        option6 = st.slider("Top p",0.0, 2.0, 1.0)
        top_p=option6
    with col7:
        option7 = st.slider("Temperature",0.0, 2.0, 1.0)
        temperature=option7
    option11=st.text_area(label="Blog")
    blog=option11
    submit_Data=st.button("Submit")
    if submit_Data:
        # print("------------------------------......................     submit data")
        tone= makeTone(option)
        # print(f"--------------------------------------------- Tone : {tone}")
        theme=themeData
        # print(f"--------------------------------------------- Theme : {theme[0:50]}")
        blog=blog
        # print(f"--------------------------------------------- Blog : {blog[0:50]}")
        example=get_traning_data_from_database(option)
        # print(f"--------------------------------------------- example : {example[0:50]}")
        modelPrompt=setting_Prompts(selectedPromptData,example,blog,theme,tone)
        # print(f"--------------------------------------------- selectedPromptData : {selectedPromptData[0:50]}")
        # print(f"--------------------------------------------- modelPrompt : {modelPrompt[0:100]}")
        modelResponse=handleModel(model,frequency_penalty,temperature,modelPrompt,top_p,presence_penalty)
        # print(f"--------------------------------------------- Model Data === model : {model } , frequency_penalty : {frequency_penalty} , temperature : {temperature} , modelPrompt : {modelPrompt[:50]} , top_p : {top_p} , presence_penalty : {presence_penalty}")
        print(f"--------------------------------------------- Model Response : {modelResponse}")

        st.write(modelResponse)
        
        

    
if __name__ == "__main__":
    main()
