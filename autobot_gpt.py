from openai import OpenAI
import time
from datetime import datetime


def form_msg_user(username: str, msg: str):
    return {
        "role": "user",
        "content": f"{username}: {msg}"
    }


def run_assistant(api_key_openai: str, assistant_id: str, messages: list[dict]) -> str:
    client = OpenAI(
        api_key=api_key_openai
    )
    assistant = client.beta.assistants.retrieve(assistant_id)

    # get the last message from the messages
    # last_message = messages[-1]
    # last_message["file_ids"] = assistant.file_ids
    # print("file_ids: " + str(assistant.file_ids))
    # return ""
    thread = client.beta.threads.create(
        messages=messages
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run_is_complete = False

    while not run_is_complete:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"run.status: {run.status}")
        if run.expires_at is not None:
            current_time = time.time()
            time_difference = run.expires_at - current_time
            minutes_until_future_time = time_difference / 60
            time_expiration_human_format = datetime.fromtimestamp(run.expires_at).strftime('%Y-%m-%d %H:%M:%S')

            print(f"run expires in: {minutes_until_future_time} mins. At: {time_expiration_human_format}")

        if run.status == "queued" or run.status == "in_progress":
            time.sleep(1)
            continue

        run_is_complete = True

    if not run.status == "completed":
        raise Exception(f"run.status: {run.status}")

    messages_last_thread = client.beta.threads.messages.list(thread_id=thread.id, limit=1, order="desc")

    client.beta.threads.delete(thread_id=thread.id)

    for msg_last_thread in messages_last_thread.data:
        print(f"gpt_response: {msg_last_thread.content[0].text.value}")
        print(f"gpt_annotation: {msg_last_thread.content[0].text.annotations}")
        return msg_last_thread.content[0].text.value
