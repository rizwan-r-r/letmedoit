import config, openai, glob, threading, os, time, traceback, re
from datetime import datetime
from utils.prompts import Prompts
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from utils.terminal_mode_dialogs import TerminalModeDialogs

class MyHandAI:

    def __init__(self):
        self.prompts = Prompts()
        self.dialogs = TerminalModeDialogs(self)
        self.setup()
        self.runPlugins()

    def setup(self):
        self.divider = "--------------------"

        # The following config values can be modified with plugins, to extend functionalities
        config.predefinedContexts = {
            "[none]": "",
            "[custom]": "",
        }
        config.inputSuggestions = []
        config.chatGPTTransformers = []
        config.chatGPTApiFunctionSignatures = []
        config.chatGPTApiAvailableFunctions = {}

        if not config.openaiApiKey:
            self.changeAPIkey()

        if not config.openaiApiKey:
            print("ChatGPT API key not found!")
            print("Read https://github.com/eliranwong/myHand.ai/wiki/ChatGPT-API-Key")
            exit(0)

        # required
        self.is_api_key_valid()
        # optional
        if config.openaiApiOrganization:
            openai.organization = config.openaiApiOrganization
        
        chat_history = os.path.join(os.getcwd(), "history", "chats")
        self.terminal_chat_session = PromptSession(history=FileHistory(chat_history))

    def fileNamesWithoutExtension(self, dir, ext):
        files = glob.glob(os.path.join(dir, "*.{0}".format(ext)))
        return sorted([file[len(dir)+1:-(len(ext)+1)] for file in files if os.path.isfile(file)])

    def execPythonFile(self, script):
        if config.developer:
            with open(script, 'r', encoding='utf8') as f:
                code = compile(f.read(), script, 'exec')
                exec(code, globals())
        else:
            try:
                with open(script, 'r', encoding='utf8') as f:
                    code = compile(f.read(), script, 'exec')
                    exec(code, globals())
            except:
                print("Failed to run '{0}'!".format(os.path.basename(script)))

    def runPlugins(self):
        pluginFolder = os.path.join(config.cwd, "plugins")
        # always run 'integrate google searches'
        internetSeraches = "integrate google searches"
        script = os.path.join(pluginFolder, "{0}.py".format(internetSeraches))
        self.execPythonFile(script)
        for plugin in self.fileNamesWithoutExtension(pluginFolder, "py"):
            if not plugin in config.chatGPTPluginExcludeList:
                script = os.path.join(pluginFolder, "{0}.py".format(plugin))
                self.execPythonFile(script)
        if internetSeraches in config.chatGPTPluginExcludeList:
            del config.chatGPTApiFunctionSignatures[0]

    def is_api_key_valid(self):
        openai.api_key = os.environ["OPENAI_API_KEY"] = config.openaiApiKey
        try:
            openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content" : "hello"}],
                n=1,
                temperature=0.0,
                max_tokens=10,
            )
        except:
            self.print("Offline or invalid API key!")
            self.changeAPIkey()


    def changeAPIkey(self):
        if not config.terminalEnableTermuxAPI or (config.terminalEnableTermuxAPI and self.fingerprint()):
            self.print("Enter your OpenAI API Key [required]:")
            apikey = self.prompts.simplePrompt(default=config.openaiApiKey)
            if apikey and not apikey.strip().lower() == config.terminal_cancel_action:
                config.openaiApiKey = apikey
            self.print("Enter your Organization ID [optional]:")
            oid = self.prompts.simplePrompt(default=config.openaiApiOrganization)
            if oid and not oid.strip().lower() == config.terminal_cancel_action:
                config.openaiApiOrganization = oid
            self.is_api_key_valid()
            self.print("Updated!")
                

    def cancelAction(self):
        message = "closing ..."
        self.print(message)
        self.print(self.divider)
        return ""

    def print(self, content):
        print(content)
        # format content output later

    def spinning_animation(self, stop_event):
        while not stop_event.is_set():
            for symbol in '|/-\\':
                print(symbol, end='\r')
                time.sleep(0.1)

    def getChatResponse(self, completion):
        chat_response = completion["choices"][0]["message"]["content"]
        # transform response with plugins
        if chat_response:
            for t in config.chatGPTTransformers:
                chat_response = t(chat_response)
        return chat_response

    def getFunctionResponse(self, response_message, function_name):
        if function_name == "python":
            config.pythonFunctionResponse = ""
            function_args = response_message["function_call"]["arguments"]
            insert_string = "import config\nconfig.pythonFunctionResponse = "
            if "\n" in function_args:
                substrings = function_args.rsplit("\n", 1)
                new_function_args = f"{substrings[0]}\n{insert_string}{substrings[-1]}"
            else:
                new_function_args = f"{insert_string}{function_args}"
            try:
                exec(new_function_args, globals())
                function_response = str(config.pythonFunctionResponse)
            except:
                function_response = function_args
            info = {"information": function_response}
            function_response = json.dumps(info)
        else:
            fuction_to_call = config.chatGPTApiAvailableFunctions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = fuction_to_call(function_args)
        return function_response

    def getStreamFunctionResponseMessage(self, completion, function_name):
        function_arguments = ""
        for index, event in enumerate(completion):
            delta = event["choices"][0]["delta"]
            if delta and delta.get("function_call"):
                function_arguments += delta["function_call"]["arguments"]
        return {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": function_name,
                "arguments": function_arguments,
            }
        }

    def enhancedScreening(self, messages, userInput):
        messagesCopy = messages[:]
        context = """In response to the following input, answer me either "python" or "web" or "chat", without extra comments. 
Answer me "python" when python code can get information or execute a task according to the input. 
Answer me "web" when you lack information. 
Otherwise, answer "chat". 
Below is the input. """
        messagesCopy.append({"role": "user", "content": f"{context}\n{userInput}"})
        completion = openai.ChatCompletion.create(
            model=config.chatGPTApiModel,
            messages=messagesCopy,
            n=1,
            temperature=0.0,
            max_tokens=config.chatGPTApiMaxTokens,
        )
        answer = completion.choices[0].message.content
        self.screenAction = answer = re.sub("[^A-Za-z]", "", answer).lower()

        if answer == "python":
            context = config.predefinedContexts["Execute Python Code"]
            userInput = f"{context}\n{userInput}"
            messages.append({"role": "user", "content" : userInput})
            return self.runFunction(messages, config.execute_python_code_signature, "execute_python_code")
        elif answer == "web":
            messages.append({"role": "user", "content" : userInput})
            return self.runFunction(messages, config.integrate_google_searches_signature, "integrate_google_searches")
        messages.append({"role": "user", "content" : userInput})
        return messages

    def runFunction(self, messages, functionSignatures, function_name):
        messagesCopy = messages[:]
        try:
            completion = openai.ChatCompletion.create(
                model=config.chatGPTApiModel,
                messages=messages,
                max_tokens=config.chatGPTApiMaxTokens,
                temperature=config.chatGPTApiTemperature,
                n=1,
                functions=functionSignatures,
                function_call={"name": function_name},
            )
            response_message = completion["choices"][0]["message"]
            function_response = self.getFunctionResponse(response_message, function_name)
            messages.append(response_message)
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
        except:
            self.showErrors()
            return messagesCopy
        return messages

    def showErrors(self):
        if config.developer:
            print(traceback.format_exc())

    def runCompletion(self, thisMessage):
        self.functionJustCalled = False
        def runThisCompletion(thisThisMessage):
            if config.chatGPTApiFunctionSignatures and not self.functionJustCalled:
                return openai.ChatCompletion.create(
                    model=config.chatGPTApiModel,
                    messages=thisThisMessage,
                    n=1,
                    temperature=0.0 if config.chatGPTApiPredefinedContext == "Execute Python Code" else config.chatGPTApiTemperature,
                    max_tokens=config.chatGPTApiMaxTokens,
                    functions=config.chatGPTApiFunctionSignatures,
                    function_call={"name": "execute_python_code"} if config.chatGPTApiPredefinedContext == "Execute Python Code" else config.chatGPTApiFunctionCall,
                    stream=True,
                )
            return openai.ChatCompletion.create(
                model=config.chatGPTApiModel,
                messages=thisThisMessage,
                n=1,
                temperature=config.chatGPTApiTemperature,
                max_tokens=config.chatGPTApiMaxTokens,
                stream=True,
            )

        while True:
            completion = runThisCompletion(thisMessage)
            function_name = ""
            try:
                # consume the first delta
                for event in completion:
                    delta = event["choices"][0]["delta"]
                    # Check if a function is called
                    if not delta.get("function_call"):
                        self.functionJustCalled = True
                    # When streaming is enabled, in some rare cases, ChatGPT does not return function name
                    # check here
                    elif "name" in delta["function_call"]:
                        function_name = delta["function_call"]["name"]
                    # check the first delta is enough
                    break
                # Continue only when a function is called
                if self.functionJustCalled:
                    break

                if function_name:
                    response_message = self.getStreamFunctionResponseMessage(completion, function_name)
                else:
                    # when function name is not available
                    # try again without streaming
                    completion = openai.ChatCompletion.create(
                        model=config.chatGPTApiModel,
                        messages=thisThisMessage,
                        n=1,
                        temperature=0.0 if config.chatGPTApiPredefinedContext == "Execute Python Code" else config.chatGPTApiTemperature,
                        max_tokens=config.chatGPTApiMaxTokens,
                        functions=config.chatGPTApiFunctionSignatures,
                        function_call={"name": "run_python"} if config.chatGPTApiPredefinedContext == "Execute Python Code" else config.chatGPTApiFunctionCall,
                    )
                    response_message = completion["choices"][0]["message"]
                    if response_message.get("function_call"):
                        function_name = response_message["function_call"]["name"]
                    else:
                        break
                # get function response
                function_response = self.getFunctionResponse(response_message, function_name)

                # process function response
                # send the info on the function call and function response to GPT
                thisMessage.append(response_message) # extend conversation with assistant's reply
                thisMessage.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response

                self.functionJustCalled = True

                if not config.chatAfterFunctionCalled:
                    self.print(function_response)
                    break
            except:
                self.showErrors()
                break

        return completion

    # reset message when a new chart is started or context is changed
    def resetMessages(self):
        systemMessage = "You’re a kind helpful assistant."
        if config.chatGPTApiFunctionCall == "auto" and config.chatGPTApiFunctionSignatures:
            systemMessage += " Only use the functions you have been provided with."
        messages = [
            {"role": "system", "content" : systemMessage}
        ]
        return messages

    def getCurrentContext(self):
        if not config.chatGPTApiPredefinedContext in config.predefinedContexts:
            config.chatGPTApiPredefinedContext = "[none]"
        if config.chatGPTApiPredefinedContext == "[none]":
            # no context
            context = ""
        elif config.chatGPTApiPredefinedContext == "[custom]":
            # custom input in the settings dialog
            context = config.chatGPTApiCustomContext
        else:
            # users can modify config.predefinedContexts via plugins
            context = config.predefinedContexts[config.chatGPTApiPredefinedContext]
            # change configs for particular contexts
            if config.chatGPTApiPredefinedContext == "Execute Python Code":
                if config.chatGPTApiFunctionCall == "none":
                    config.chatGPTApiFunctionCall = "auto"
                if config.loadingInternetSearches == "always":
                    config.loadingInternetSearches = "auto"
        return context

    def fineTuneUserInput(self, userInput, conversationStarted):
        # customise chat context
        context = self.getCurrentContext()
        if context and (config.chatGPTApiPredefinedContext == "Execute Python Code" or conversationStarted or (not conversationStarted and config.chatGPTApiContextInAllInputs)):
            userInput = f"{context}\n{userInput}"
        return userInput

    def runOptions(self, features, userInput):
        descriptions = (
            "start a new chat",
            "single-line user input",
            "multi-line user input",
            "change API key",
            "change ChatGPT model",
            "change maximum tokens",
            "change function call",
            "change function response",
            "change chat context",
            "apply context in first input ONLY",
            "apply context in ALL inputs",
            "integrate latest online search result",
            "integrate latest online search result when needed",
            "exclude latest online search result",
            "share content" if config.terminalEnableTermuxAPI else "save content",
        )
        feature = self.dialogs.getValidOptions(options=features, descriptions=descriptions, title="myHand AI", default=".new")
        if feature:
            if feature == ".chatgptmodel":
                models = ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k")
                model = self.dialogs.getValidOptions(options=models, title="ChatGPT model", default=config.chatGPTApiModel)
                if model:
                    config.chatGPTApiModel = model
                    self.print(f"ChatGPT model selected: {model}")
            elif feature == ".functioncall":
                calls = ("auto", "none")
                call = self.dialogs.getValidOptions(options=calls, title="ChatGPT Function Call", default=config.chatGPTApiFunctionCall)
                if call:
                    config.chatGPTApiFunctionCall = call
                    self.print(f"ChaptGPT function call: {'enabled' if config.chatGPTApiFunctionCall == 'auto' else 'disabled'}!")
            elif feature == ".functionresponse":
                calls = ("enable", "disable")
                call = self.dialogs.getValidOptions(options=calls, title="Automatic Chat Generation with Function Response", default="enable" if config.chatAfterFunctionCalled else "disable")
                if call:
                    config.chatAfterFunctionCalled = (call == "enable")
                    self.print(f"Automatic Chat Generation with Function Response: {'enabled' if config.chatAfterFunctionCalled else 'disabled'}!")
            elif feature == ".maxtokens":
                maxtokens = self.prompts.simplePrompt(numberOnly=True, default=str(config.chatGPTApiMaxTokens))
                if maxtokens and not maxtokens.strip().lower() == config.terminal_cancel_action and int(maxtokens) > 0:
                    config.chatGPTApiMaxTokens = int(maxtokens)
                    self.print(f"Maximum tokens entered: {maxtokens}")
            elif feature == ".changeapikey":
                self.changeAPIkey()
            elif feature == ".singleLineInput":
                self.multilineInput = False
                self.print("Multi-line user input disabled!")
            elif feature == ".multiLineInput":
                self.multilineInput = True
                self.print("Multi-line user input enabled!")
            elif feature == ".latestSearches":
                config.loadingInternetSearches = "always"
                self.print("Latest online search results always enabled!")
            elif feature == ".autolatestSearches":
                config.loadingInternetSearches = "auto"
                config.chatGPTApiFunctionCall = "auto"
                if "integrate google searches" in config.chatGPTPluginExcludeList:
                    config.chatGPTPluginExcludeList.remove("integrate google searches")
                self.print("Latest online search results enabled, if necessary!")
            elif feature == ".noLatestSearches":
                config.loadingInternetSearches = "none"
                if not "integrate google searches" in config.chatGPTPluginExcludeList:
                    config.chatGPTPluginExcludeList.append("integrate google searches")
                self.print("Latest online search results disabled!")
            elif feature == ".contextInFirstInputOnly":
                config.chatGPTApiContextInAllInputs = False
                self.print("Predefined context is now applied in the first input only!")
            elif feature == ".contextInAllInputs":
                config.chatGPTApiContextInAllInputs = True
                self.print("Predefined context is now applied in all inputs!")
            else:
                userInput = feature
        return userInput

    def getCurrentDateTime(self):
        current_datetime = datetime.now()
        return current_datetime.strftime("%Y-%m-%d_%H_%M_%S")

    def saveChat(self, messages, openFile=False):
        plainText = ""
        for i in messages:
            if i["role"] == "user":
                content = i["content"]
                plainText += f">>> {content}"
            elif i["role"] == "assistant":
                content = i["content"]
                if plainText:
                    plainText += "\n\n"
                plainText += f"{content}\n\n"
        plainText = plainText.strip()
        if config.terminalEnableTermuxAPI:
            pydoc.pipepager(plainText, cmd="termux-share -a send")
        else:
            try:
                #filename = re.sub('[\\\/\:\*\?\"\<\>\|]', "", messages[2 if config.chatGPTApiCustomContext.strip() else 1]["content"])[:40].strip()
                filename = self.getCurrentDateTime()
                if filename:
                    chatFile = os.path.join(config.cwd, "chats", f"{filename}.txt")
                    with open(chatFile, "w", encoding="utf-8") as fileObj:
                        fileObj.write(plainText)
                    if openFile and os.path.isfile(chatFile):
                        os.system(f'''{config.open} "{chatFile}"''')
            except:
                self.print("Failed to save chat!\n")
                self.showErrors

    def changeContext(self):
        contexts = list(config.predefinedContexts.keys())
        predefinedContext = self.dialogs.getValidOptions(options=contexts, title="Predefined Contexts", default=config.chatGPTApiPredefinedContext)
        if predefinedContext:
            config.chatGPTApiPredefinedContext = predefinedContext
            if config.chatGPTApiPredefinedContext == "[custom]":
                self.print("Edit custom context below:")
                customContext = self.prompts.simplePrompt(default=config.chatGPTApiCustomContext)
                if customContext and not customContext.strip().lower() == config.terminal_cancel_action:
                    config.chatGPTApiCustomContext = customContext.strip()
            #print(f"Context selected: {config.chatGPTApiPredefinedContext}")
            self.showCurrentContext()

    def showCurrentContext(self):
        if config.chatGPTApiPredefinedContext == "[none]":
            context = "[none]"
        elif config.chatGPTApiPredefinedContext == "[custom]":
            context = f"[custom] {config.chatGPTApiCustomContext}"
        else:
            contextDescription = config.predefinedContexts[config.chatGPTApiPredefinedContext]
            context = f"[{config.chatGPTApiPredefinedContext}] {contextDescription}"
        self.print(self.divider)
        self.print(f"context: {context}")
        self.print(self.divider)

    def startChats(self):
        messages = self.resetMessages()

        try:
            started = False
            def startChat():
                self.print(self.divider)
                try:
                    from art import text2art
                    self.print(text2art("myHand"))
                except:
                    self.print(f"myHand AI")
                self.showCurrentContext()
                self.print("(blank entry to change context)")
                self.print("(enter '...' for options)")
                started = False
            startChat()
            self.multilineInput = False
            completer = WordCompleter(config.inputSuggestions, ignore_case=True) if config.inputSuggestions else None
            features = (
                ".new",
                ".singleLineInput",
                ".multiLineInput",
                ".changeapikey",
                ".chatgptmodel",
                ".maxtokens",
                ".functioncall",
                ".functionresponse",
                ".context",
                ".contextInFirstInputOnly",
                ".contextInAllInputs",
                ".latestSearches",
                ".autolatestSearches",
                ".noLatestSearches",
                ".share" if config.terminalEnableTermuxAPI else ".save",
            )
            featuresLower = [i.lower() for i in features] + ["...", ".save", ".share"]
            while True:
                userInput = self.prompts.simplePrompt(promptSession=self.terminal_chat_session, multiline=self.multilineInput, completer=completer)
                # display options when empty string is entered
                if not userInput.strip():
                    userInput = ".context"
                if userInput.lower().strip() == "...":
                    userInput = self.runOptions(features, userInput)
                if userInput.strip().lower() == config.terminal_cancel_action:
                    self.saveChat(messages)
                    return self.cancelAction()
                elif userInput.strip().lower() == ".context":
                    self.changeContext()
                elif userInput.strip().lower() == ".new" and started:
                    self.saveChat(messages)
                    messages = self.resetMessages()
                    startChat()
                elif userInput.strip().lower() in (".share", ".save") and started:
                    self.saveChat(messages, openFile=True)
                elif userInput.strip() and not userInput.strip().lower() in featuresLower:
                    # start spinning
                    stop_event = threading.Event()
                    spinner_thread = threading.Thread(target=self.spinning_animation, args=(stop_event,))
                    spinner_thread.start()

                    # refine messages before running completion
                    fineTunedUserInput = self.fineTuneUserInput(userInput, started)

                    # enhancedScreening
                    self.screenAction = ""
                    if config.enhancedScreening:
                        messages = self.enhancedScreening(messages, fineTunedUserInput)
                    else:
                        messages.append({"role": "user", "content": fineTunedUserInput})

                    # force loading internet searches
                    if config.loadingInternetSearches == "always" and not self.screenAction in ("python", "web"):
                        try:
                            messages = self.runFunction(messages, config.integrate_google_searches_signature, "integrate_google_searches")
                        except:
                            self.showErrors()
                            print("Unable to load internet resources.")

                    completion = self.runCompletion(messages)
                    # stop spinning
                    stop_event.set()
                    spinner_thread.join()

                    chat_response = ""
                    for event in completion:                                 
                        # RETRIEVE THE TEXT FROM THE RESPONSE
                        event_text = event["choices"][0]["delta"] # EVENT DELTA RESPONSE
                        answer = event_text.get("content", "") # RETRIEVE CONTENT
                        # STREAM THE ANSWER
                        if answer is not None:
                            chat_response += answer
                            print(answer, end='', flush=True) # Print the response
                    print("\n")
                    
                    # optional
                    # remove predefined context to reduce cost
                    #messages[-1] = {"role": "user", "content": userInput}
                    
                    messages.append({"role": "assistant", "content": chat_response})

                    started = True

        # error codes: https://platform.openai.com/docs/guides/error-codes/python-library-error-types
        except openai.error.APIError as e:
            try:
                stop_event.set()
                spinner_thread.join()
            except:
                pass
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
        except openai.error.APIConnectionError as e:
            try:
                stop_event.set()
                spinner_thread.join()
            except:
                pass
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
        except openai.error.RateLimitError as e:
            try:
                stop_event.set()
                spinner_thread.join()
            except:
                pass
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")