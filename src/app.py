import chainlit as cl
import plotly.graph_objects as go
import matplotlib.pyplot as plt


@cl.on_chat_start
async def main():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

    elements = [
        cl.Pyplot(name="plot", figure=fig, display="inline", size='large'),
    ]
    await cl.Message(
        content="Here is a simple plot",
        elements=elements,
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    fig = go.Figure(
        data=[go.Bar(y=[2, 1, 3])],
        layout=go.Layout(
            title='figure title',
            template='simple_white'
        )
    )
    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
        elements=elements
    ).send()