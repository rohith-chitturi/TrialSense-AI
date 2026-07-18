import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

# We will define workflows and activities later in the implementation
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Connect to local Temporal server from docker-compose
    client = await Client.connect("localhost:7233")
    logging.info("Connected to Temporal server")
    
    # Run a worker for the "trialsense-task-queue"
    worker = Worker(
        client,
        task_queue="trialsense-task-queue",
        workflows=[],
        activities=[],
    )
    
    logging.info("Starting Temporal Worker...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
