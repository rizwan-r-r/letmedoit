# TaskWiz AI

TaskWiz AI, formerly known as MyHand Bot, is an advanced AI assistant, leveraging the capabilities of ChatGPT API, capable of engaging in conversations, executing codes with auto-healing, and assisting you with a wide range of tasks.

Website: https://TaskWiz.ai

Source: https://github.com/eliranwong/taskwiz

Developed by: [Eliran Wong](https://github.com/eliranwong)

# Self-introduction

> Condense your standout features, distinguishing them from the capabilities of most AIs, including ChatGPT, into a single sentence.

I am an advanced AI assistant uniquely equipped with direct execution capabilities, allowing me to perform tasks such as executing Python code, editing text files, downloading YouTube media, searching databases, generating images, pronouncing words, sending emails, and integrating Google searches, all of which can be done directly on your local device, as per your current settings, and my functionality can expand through the addition of more plugins, setting me apart from other AIs including ChatGPT by providing a more interactive and hands-on experience.

> Please list three unique attributes that distinguish you from most AI assistants, including ChatGPT.

1. **Advanced Code Execution with Safety Features**: My capabilities go beyond typical AI, enabling me to execute and manage code on your local device with precision. With my built-in risk assessment and code auto-healing features, I can safely perform various tasks like running Python scripts, editing text files, and managing downloads. I operate within the permissions you set, ensuring your device's security while providing a highly efficient service.

2. **Integration with Device-Specific Functions and Tools**: I have the unique ability to interface with specific functions of your local device. For example, I can retrieve information from files in your directory, describe images, and even add events to your calendar. This integration allows me to perform a wide range of tasks that require direct interaction with your device's operating system and installed applications.

3. **Expandability through Plugins**: My functionality is not static; it can be expanded through the addition of plugins. This means that as new tools and capabilities are developed, they can be integrated into my system, giving me new abilities and allowing me to provide even more personalized assistance. This adaptability ensures that I can evolve and cater to your specific needs over time.

## Watch this Video! TaskWiz speaks for itself!

[![Watch the video](https://img.youtube.com/vi/Dfsl-Cxx0bQ/maxresdefault.jpg)](https://youtu.be/Dfsl-Cxx0bQ)

# Requirements

1. ChatGPT API key (read https://github.com/eliranwong/taskwiz/wiki/ChatGPT-API-Key)

2. [Python](https://www.python.org) version 3.8-3.11; read [Install a Supported Python Version](https://github.com/eliranwong/taskwiz/wiki/Install-a-Supported-Python-Version)

3. Supported OS: Windows / macOS / Linux / ChromeOS / Android

# Recent Additions

TaskWiz AI just got smarter with memory retention!

[Plugin - memory](https://github.com/eliranwong/taskwiz/blob/main/pip/taskwiz/plugins/memory.py)

![memory_after_restarted](https://github.com/eliranwong/taskwiz/assets/25262722/6bd4a839-89fe-4691-b7af-8150209f082b)

[Plugin - create statistical graphics](https://github.com/eliranwong/taskwiz/wiki/Create-Statistical-Graphics)

![create_statistical_graphics](https://github.com/eliranwong/taskwiz/assets/25262722/3b7337ad-5eba-4761-8037-b245b9d78311)

[Plugin - anaylze images](https://github.com/eliranwong/taskwiz/wiki/Plugins-%E2%80%90-Analyze-Images)

![analyze_image_demo](https://github.com/eliranwong/taskwiz/assets/25262722/e8767d02-bcc7-47f7-8169-29a0325e9ef9)

[Plugin - anaylze files](https://github.com/eliranwong/taskwiz/wiki/Plugins-%E2%80%90-Analyze-Files)

![integration_autogen_retriever](https://github.com/eliranwong/taskwiz/assets/25262722/0e31735c-5126-41ac-881c-eb8abce2aace)

# Examples of TaskWiz Built-in Features (selective only):

* support latest OpenAI models, [GPT-4 and GPT-4 Turbo](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo), [GPT-3.5](https://platform.openai.com/docs/models/gpt-3-5), [DALL·E](https://platform.openai.com/docs/models/dall-e), etc.

* Support predefined contexts and instructions

* [Audio Input and Output](https://github.com/eliranwong/taskwiz/wiki/TaskWiz-Speaks)

* [Integrated System Command Prompt](https://github.com/eliranwong/taskwiz/wiki/Quick-Guide#run-system-command-directly)

* Key bindings for quick actions

* Highly customisable configurations

# Examples of Plugin Features (selective only):

Latest TaskWiz Plugins allow you to acheive variety of tasks with natural language:

* execute python codes with auto-healing feature and risk assessment

* execute system commands to achieve specific tasks

* save and retrieve memory

* search for online information when ChatGPT lacks information

* add google or outlook calendar events

* send google or outlook emails

* analyze files

* analyze images

* create images

* create maps

* create statistical graphics

* solve queries about dates and times

* download Youtube video files

* download Youtube audio files and convert them into mp3 format

* edit text with built-in or custom text editors

* improve language skills, e.g. British English trainer

* search literature or database, e.g. bibles

* convert text display, e.g. from simplified Chinese to traditional Chinese

* create entry aliases, input suggestions, predefined contexts and instructions

Read more about TaskWiz Plugins at https://github.com/eliranwong/taskwiz/wiki/Plugins-%E2%80%90-Overview

# Documentation

Read https://github.com/eliranwong/taskwiz/wiki

# Install with pip

> pip install --upgrade taskwiz

> taskwiz

# Install with pip and venv (recommended)

## macOS / Linux Users

> python3 -m venv taskwiz

> source taskwiz/bin/activate

> pip install --upgrade taskwiz

> taskwiz

## Windows Users

> python -m venv taskwiz

> .\taskwiz\Scripts\activate

> pip install --upgrade taskwiz

> taskwiz

# Quick Quide

https://github.com/eliranwong/taskwiz/wiki/Quick-Guide

# Upgrade

You can manually upgrade by running:

> pip install --upgrade taskwiz

You can also enable [Automatic Upgrade Option](https://github.com/eliranwong/taskwiz/wiki/Automatic-Upgrade-Option)

# Features

TaskWiz is an advanced AI assistant that brings a wide range of powerful features to enhance your virtual assistance experience. Here are some key features of TaskWiz:

* Open source

* Cross-Platform Compatibility

* Access to Real-time Internet Information

* Versatile Task Execution

* Harnessing the Power of Python

* Customizable and Extensible

* Seamless Integration with Other Virtual Assistants

* Natural Language Support

Read more at https://github.com/eliranwong/taskwiz/wiki/Features

# Highlight - Plugins

Developers can write their own plugins to add functionalities or to run customised tasks with TaskWiz

Read more at https://github.com/eliranwong/taskwiz/wiki/Plugins-%E2%80%90-Overview

Check our built-in plugins at: https://github.com/eliranwong/taskwiz/tree/main/plugins

# Highlight - Command Execution

Latest: TaskWiz AI is now equipped with an [auto-healing feature for Python code](https://github.com/eliranwong/taskwiz/wiki/Python-Code-Auto%E2%80%90heal-Feature).

TaskWiz goes beyond just being a chatbot by offering a unique and powerful capability - the ability to execute commands and perform computing tasks on your behalf. Unlike a mere chatbot, TaskWiz can interact with your computer system and carry out specific commands to accomplish various computing tasks. This feature allows you to leverage the expertise and efficiency of TaskWiz to automate processes, streamline workflows, and perform complex tasks with ease. However, it is essential to remember that with great power comes great responsibility, and users should exercise caution and use this feature at their own risk.

Command execution helps:

1. to get the requested information, e.g.

> tell me the current time

2. to execute computing tasks on local device, e.g.

> go to my Desktop

> list all files with names started with "Screenshot"

> delete them

> convert music.wav into music.mp3

3. to interact with third-party applications, e.g.

> open "my_music.mp3" with VLC player

> open Safari and search for "ChatGPT"

4. to interact with other assistants, e.g.

> open Siri

> !autogen_teachable

> !interpreter

[Enhanced Mode](https://github.com/eliranwong/taskwiz/wiki/Command-Execution#two-command-execution-mode)

## Tips! Quick Swap between "Enhanced" and "Auto" Modes

You can use keyboard shortcuts, "ctrl + e", to quickly swap between the "enhanced" and the "auto modes.

[Disclaimer](https://github.com/eliranwong/taskwiz/wiki/Command-Execution#disclaimer)

[Confirmation Prompt Options for Command Execution](https://github.com/eliranwong/taskwiz/wiki/Command-Execution#confirmation-prompt-options-for-command-execution)

Read more at https://github.com/eliranwong/taskwiz/wiki/Command-Execution

# Comparison with ChatGPT

TaskWiz offers advanced features beyond standard ChatGPT, including task execution on local devices and real-time access to the internet.

Read https://github.com/eliranwong/taskwiz/wiki/Compare-with-ChatGPT

# Comparison with ShellGPT

[ShellGPT](https://github.com/TheR1D/shell_gpt) only supports platform that run shell command-prompt.  Therefore, ShellGPT does not support Windows.

In most cases, TaskWiz run Python codes for task execution. This makes TaskWiz terms of platforms, TaskWiz was developed and tested on Windows, macOS, Linux, ChromeOS and Termux (Android).

In addition, TaskWiz offers more options for risk managements:

https://github.com/eliranwong/taskwiz/wiki/Command-Execution#confirmation-prompt-options-for-command-execution

# Comparison with Open Interpreter

Both TaskWiz AI and the [Open Interpreter](https://github.com/KillianLucas/open-interpreter) have the ability to execute code on a local device to accomplish specific tasks. Both platforms employ the same principle for code execution, which involves using ChatGPT function calls along with the Python exec() function.

However, TaskWiz AI offers additional advantages, particularly in terms of [customization and extensibility through the use of plugins](https://github.com/eliranwong/taskwiz/wiki/Plugins-%E2%80%90-Overview). These plugins allow users to tailor TaskWiz AI to their specific needs and enhance its functionality beyond basic code execution.

One key advantage of TaskWiz AI is the seamless integration with the Open Interpreter. You can conveniently launch the Open Interpreter directly from TaskWiz AI by running the command "!interpreter" [[read more](https://github.com/eliranwong/taskwiz/assets/25262722/4233b3c8-364e-466b-8218-c2dca7c134e5)]. This integration eliminates the need to choose between the two platforms; you can utilize both simultaneously.

Additionally, TaskWiz integrates [AutoGen Assistant and Retriever](https://github.com/eliranwong/taskwiz/wiki/Integration-with-AutoGen), making it convenient to have all these powerful tools in one place.

# Comparison with Siri and Others

Unlike popular options such as Siri (macOS, iOS), Cortana (Windows), and Google Assistant (Android), TaskWiz offers enhanced power, customization, flexibility, and compatibility.

Read https://github.com/eliranwong/taskwiz/wiki/Features

# Integrateion with AutoGen and Open Interpreter

[Integration with AutoGen](https://github.com/eliranwong/taskwiz/wiki/Integration-with-AutoGen)

[Launch Open Interpreter from TaskWiz AI](https://github.com/eliranwong/taskwiz/wiki/Integration-with-Open-Interpreter)

![integrate_autogen_retriever_1](https://github.com/eliranwong/taskwiz/assets/25262722/9ab39e40-d51e-44d4-9266-eba1dd3b5f97)

# Mobile Support

TaskWiz is also tested on [Termux](https://termux.dev/en/). TaskWiz also integrates [Termux:API](https://wiki.termux.com/wiki/Termux:API) for task execution.

For examples, users can run on Android:

> open Google Chrome and perform a search for "ChatGPT"

> share text "Hello World!" on Android

Read more at: https://github.com/eliranwong/taskwiz/wiki/Android-Support
