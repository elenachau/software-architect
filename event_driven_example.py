import asyncio
import random
from asyncio import Queue
from typing import Awaitable, Callable
from enum import StrEnum


class EventType(StrEnum):
    LOGIN = "Login"
    LOGOUT = "Logout"
    PURCHASE = "Purchase"


EventQueue = Queue[tuple[EventType, str]]  # temporarily store event

EventConsumerFn = Callable[[EventType, str], Awaitable[None]]

registered_consumers: dict[EventType, EventConsumerFn] = {}


# register consumers dynamically
def register_consumer(event_type: EventType, consumer: EventConsumerFn):
    registered_consumers[event_type] = consumer


async def general_event_consumer(queue: EventQueue):
    while True:
        event_type, event_data = await queue.get()
        consumer = registered_consumers.get(event_type)
        if consumer:
            await consumer(event_type, event_data)
        await asyncio.sleep(random.uniform(0.5, 1))


# specific consumers
async def consume_login_event(_: EventType, event_data: str) -> None:
    print(f"Consuming Login Event: {event_data}")
    await asyncio.sleep(0.1)


async def consume_logout_event(_: EventType, event_data: str) -> None:
    print(f"Consuming Logout Event: {event_data}")
    await asyncio.sleep(0.1)


async def consume_purchase_event(_: EventType, event_data: str) -> None:
    print(f"Consuming Purchase Event: {event_data}")
    await asyncio.sleep(0.1)


# event generator
async def produce_event(queue: EventQueue):
    while True:
        event_type: EventType = random.choice(
            [EventType.LOGIN, EventType.LOGOUT, EventType.PURCHASE]
        )
        event_data: str = f"Event Data for {event_type}"
        print(f"Produced: {event_type}")
        await queue.put((event_type, event_data))
        await asyncio.sleep(random.uniform(0.5, 1.5))


# run event loop
async def main():
    queue: EventQueue = Queue()

    # register consumers
    register_consumer(EventType.LOGIN, consume_login_event)
    register_consumer(EventType.LOGOUT, consume_logout_event)
    register_consumer(EventType.PURCHASE, consume_purchase_event)

    await asyncio.gather(produce_event(queue), general_event_consumer(queue))


if __name__ == "__main__":
    asyncio.run(main())
