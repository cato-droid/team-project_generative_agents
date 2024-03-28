"""
Authors: 
Joon Sung Park (joonspk@stanford.edu)
Cato Kurtz (cato.kurtz@student.uni-tuebingen.de)

File: gpt_structure.py
Description: Wrapper functions for calling LLama2 APIs.
"""
import json
import time
import os

from utils import *

# load the large language model file
from llama_cpp import Llama

current_path = os.getcwd()
print(current_path)

model = Llama(model_path = "./persona/prompt_template/llama-models/llama-2-7b-chat.ggmlv3.q2_K.bin",
              embedding = True,
              n_ctx=1000, #permit larger contexts
              n_gpu_layers = 35) #adjust to layers of gpu that the simulation is run on


def temp_sleep(seconds=0.1):
  time.sleep(seconds)


def ChatGPT_single_request(prompt): 
  temp_sleep()

  response = model.create_chat_completion(
                messages = [{"role": "user", "content": prompt}],
                max_tokens = 1000)
  return response["choices"][0]["message"]["content"]

# ============================================================================
# #####################[SECTION 1: Llama2 STRUCTURE] ######################
# ============================================================================

'''def GPT4All_request(prompt): #FIXME needed?
  """
  Given a prompt, make a request to GPT4All model and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT4All's response. 
  """
  temp_sleep()

  try: 
    output = model.create_chat_completion(
            messages = [{"role": "user", "content": prompt}],
            max_tokens=max_tokens)
    return output["choices"][0]["message"]["content"]
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"
'''

def ChatGPT_request(prompt): 
  """
  Given a prompt, make a request to Llama model

  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of Llama's response. 
  """
  # temp_sleep()
  try: 
    output = model.create_chat_completion(
            messages = [{"role": "user", "content": prompt}],
            max_tokens = 1000)
    return output["choices"][0]["message"]["content"]
  except: 
    print ("llm ERROR")
    return "llm ERROR"


'''def GPT4_safe_generate_response(prompt, #FIXME needed?
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  prompt = 'GPT4All Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("GPT4All PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = GPT4All_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False'''


def ChatGPT_safe_generate_response(prompt, 
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose: 
    print ("Llama PROMPT")
    print (prompt)

  for i in range(repeat): 

    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose: 
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass

  return False


def ChatGPT_safe_generate_response_OLD(prompt, 
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  if verbose: 
    print ("Llama PROMPT")
    print (prompt)

  for i in range(repeat): 
    try: 
      curr_gpt_response = ChatGPT_request(prompt).strip()
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)
      if verbose: 
        print (f"---- repeat count: {i}")
        print (curr_gpt_response)
        print ("~~~~")

    except: 
      pass
  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ###################[SECTION 2: ORIGINAL Llama STRUCTURE] ###################
# ============================================================================

def GPT_request(prompt, gpt_parameter): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to the local
  Llama model and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of Llama's response. 
  """
  temp_sleep()
  try: 


    output = model.create_chat_completion(
      messages = [{"role": "user", "content":prompt}],
      max_tokens=gpt_parameter["max_tokens"],
      temperature=gpt_parameter["temperature"],
      top_p=gpt_parameter["top_p"]
      )
    
    return output["choices"][0]["message"]["content"]
  except: 
    print ("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the Llama model. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to the Llama model.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


def safe_generate_response(prompt, 
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False): 
  if verbose: 
    print (prompt)

  for i in range(repeat): 
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    if func_validate(curr_gpt_response, prompt=prompt): 
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose: 
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response


def get_embedding(text):
    text = text.replace("\n", " ")
    if not text: 
        text = "this is blank"
    return model.create_embedding(input=text, model=model) 



if __name__ == '__main__':
  gpt_parameter = {"max_tokens": max_tokens, 
                   "temperature": temperature, "top_p": 1, "stream": False,
                   "frequency_penalty": 0, "presence_penalty": 0, 
                   "stop": ['"']}
  curr_input = ["driving to a friend's house"]
  prompt_lib_file = "prompt_template/test_prompt_July5.txt"
  prompt = generate_prompt(curr_input, prompt_lib_file)

  def __func_validate(gpt_response): 
    if len(gpt_response.strip()) <= 1:
      return False
    if len(gpt_response.strip().split(" ")) > 1: 
      return False
    return True
  def __func_clean_up(gpt_response):
    cleaned_response = gpt_response.strip()
    return cleaned_response

  output = safe_generate_response(prompt, 
                                 gpt_parameter,
                                 5,
                                 "rest",
                                 __func_validate,
                                 __func_clean_up,
                                 True)

  print (output)
