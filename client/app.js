document.getElementById("send-button").addEventListener("click",sendMessage);
document.getElementById("user-input").addEventListener("keypress",e=>{
    if(e.key === 'Enter'){
        sendMessage();
    }
});
async function addMessage(text_message, sender){
    const chatBox = document.getElementById("chat-box");   
    const messageElem = document.createElement("div");
    messageElem.classList.add("message", sender);
    messageElem.textContent = text_message;
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
} 


async function sendMessage(){
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if(text === "") return;
    addMessage(text, "user");
    input.value = "";

    console.log("Sending to server:", text);  // <<< בדיקה

    const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
    });

    const data = await res.json();
    console.log("Server replied:", data);       // <<< בדיקה
    addMessage(data.response , "bot");
}
