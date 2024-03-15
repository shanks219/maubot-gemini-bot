from maubot import Plugin, MessageEvent
from maubot.handlers import command
from langchain_google_genai import ChatGoogleGenerativeAI
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot.handlers import command
from typing import Type

class Config(BaseProxyConfig):
  def do_update(self, helper: ConfigUpdateHelper) -> None:
    helper.copy("whitelist")
    helper.copy("command_prefix")
    helper.copy("google_api_key")
    
class GeminiBot(Plugin):
  async def start(self) -> None:
    self.config.load_and_update()
    
  @classmethod
  def get_config_class(cls) -> Type[BaseProxyConfig]:
    return Config
  
  @command.new("gemini", help="Gemini will answer your question", aliases=["gi"])
  @command.argument("message", pass_raw=True)
  async def answer(self, evt: MessageEvent, message: str) -> None:
    # if self.config is None or self.config['google_api_key'] is None:
    #   return
    key = self.config['google_api_key']
    llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=key)
    prompt=f"{message}"
    response = llm.invoke(prompt)
    await evt.respond(f"{response.content}")
    
  # @command.new(name="hello", require_subcommand=True)
  # async def base_command(self, evt: MessageEvent) -> None:
  #   # When you require a subcommand, the base command handler
  #   # doesn't have to do anything.
  #   pass

  # @base_command.subcommand(help="Do subcommand things")
  # async def subcommand(self, evt: MessageEvent) -> None:
  #   await evt.react("subcommand!")
    