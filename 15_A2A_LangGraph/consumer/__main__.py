import os
import sys
import click
from dotenv import load_dotenv

from consumer.agent import ConsumerAgent

# Load environment variables from .env file
load_dotenv()


@click.command()
@click.option('--query', 'query', required=True, help='User query to send via consumer agent')
@click.option('--thread-id', 'thread_id', default='consumer-thread-1')
def main(query: str, thread_id: str) -> None:
    agent = ConsumerAgent()
    for item in agent.stream(query, thread_id):
        message = item["messages"][-1]
        content = getattr(message, "content", None)
        if content:
            print(content)


if __name__ == '__main__':
    main() 