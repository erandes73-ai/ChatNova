// =========================================================
// CHATNOVA - COMPLETE CHAT JAVASCRIPT
// =========================================================

// =========================================================
// GLOBAL STATE
// =========================================================

let currentConversationId = null;


// =========================================================
// GET HTML ELEMENTS
// =========================================================

const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const chatBox =
    document.getElementById("chatBox");

const typingIndicator =
    document.getElementById("typingIndicator");

const conversationList =
    document.getElementById("conversationList");

const newChatButton =
    document.getElementById("newChatButton");


// =========================================================
// CHECK ELEMENTS
// =========================================================

if (!messageInput) {
    console.error(
        "ChatNova: messageInput not found."
    );
}

if (!sendButton) {
    console.error(
        "ChatNova: sendButton not found."
    );
}

if (!chatBox) {
    console.error(
        "ChatNova: chatBox not found."
    );
}


// =========================================================
// SEND BUTTON
// =========================================================

if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendMessage
    );

}


// =========================================================
// ENTER KEY
// =========================================================

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );

}


// =========================================================
// AUTO RESIZE TEXTAREA
// =========================================================

if (messageInput) {

    messageInput.addEventListener(
        "input",
        function () {

            this.style.height = "auto";

            this.style.height =
                Math.min(
                    this.scrollHeight,
                    120
                ) + "px";

        }
    );

}


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendMessage() {

    if (!messageInput) {
        return;
    }

    const message =
        messageInput.value.trim();


    // -----------------------------------------
    // EMPTY MESSAGE
    // -----------------------------------------

    if (!message) {
        return;
    }


    // -----------------------------------------
    // DISABLE INPUT
    // -----------------------------------------

    messageInput.disabled = true;

    if (sendButton) {
        sendButton.disabled = true;
    }


    // -----------------------------------------
    // SHOW USER MESSAGE
    // -----------------------------------------

    addUserMessage(message);


    // -----------------------------------------
    // CLEAR INPUT
    // -----------------------------------------

    messageInput.value = "";

    messageInput.style.height = "auto";


    // -----------------------------------------
    // SHOW TYPING
    // -----------------------------------------

    showTyping();


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        message:
                            message,

                        conversation_id:
                            currentConversationId

                    })

                }
            );


        const data =
            await response.json();


        hideTyping();


        // -----------------------------------------
        // ERROR
        // -----------------------------------------

        if (!response.ok) {

            addBotMessage(
                data.error ||
                "Sorry, something went wrong."
            );

            return;
        }


        // -----------------------------------------
        // UPDATE CONVERSATION ID
        // -----------------------------------------

        if (
            data.conversation_id
        ) {

            currentConversationId =
                data.conversation_id;

        }


        // -----------------------------------------
        // BOT RESPONSE
        // -----------------------------------------

        addBotMessage(
            data.response ||
            "Sorry, I could not generate a response."
        );


        // -----------------------------------------
        // REFRESH SIDEBAR
        // -----------------------------------------

        await loadConversations();


    } catch (error) {

        console.error(
            "ChatNova Error:",
            error
        );

        hideTyping();

        addBotMessage(
            "Sorry, something went wrong. Please try again."
        );


    } finally {

        messageInput.disabled = false;

        if (sendButton) {
            sendButton.disabled = false;
        }

        messageInput.focus();

    }

}


// =========================================================
// ADD USER MESSAGE
// =========================================================

function addUserMessage(message) {

    if (!chatBox) {
        return;
    }

    const row =
        document.createElement("div");

    row.className =
        "message-row user-row";


    const currentTime =
        getCurrentTime();


    row.innerHTML = `

        <div class="message-content">

            <div class="message-sender">
                You
            </div>

            <div class="user-message">

                ${formatMessage(message)}

                <div class="message-time">
                    ${currentTime}
                </div>

            </div>

        </div>

        <div class="message-avatar user-avatar">
            👤
        </div>

    `;


    chatBox.appendChild(row);

    scrollToBottom();

}


// =========================================================
// ADD BOT MESSAGE
// =========================================================

function addBotMessage(message) {

    if (!chatBox) {
        return;
    }

    const row =
        document.createElement("div");


    row.className =
        "message-row bot-row";


    const currentTime =
        getCurrentTime();


    row.innerHTML = `

        <div class="message-avatar bot-avatar">
            🤖
        </div>

        <div class="message-content">

            <div class="message-sender">
                ChatNova
            </div>

            <div class="bot-message">

                ${formatMessage(message)}

                <div class="message-time">
                    ${currentTime}
                </div>

            </div>

        </div>

    `;


    chatBox.appendChild(row);

    scrollToBottom();

}


// =========================================================
// FORMAT MESSAGE SAFELY
// =========================================================

function formatMessage(message) {

    const div =
        document.createElement("div");


    div.textContent =
        message || "";


    let safeMessage =
        div.innerHTML;


    safeMessage =
        safeMessage.replace(
            /\n/g,
            "<br>"
        );


    return safeMessage;

}


// =========================================================
// CURRENT TIME
// =========================================================

function getCurrentTime() {

    const now =
        new Date();


    return now.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


// =========================================================
// HISTORY TIME
// =========================================================

function formatHistoryTime(timestamp) {

    if (!timestamp) {
        return "";
    }


    const date =
        new Date(
            timestamp.replace(
                " ",
                "T"
            )
        );


    if (
        isNaN(
            date.getTime()
        )
    ) {

        return "";

    }


    return date.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


// =========================================================
// TYPING INDICATOR
// =========================================================

function showTyping() {

    if (!typingIndicator) {
        return;
    }


    typingIndicator.style.display =
        "flex";


    scrollToBottom();

}


// =========================================================
// HIDE TYPING INDICATOR
// =========================================================

function hideTyping() {

    if (!typingIndicator) {
        return;
    }


    typingIndicator.style.display =
        "none";

}


// =========================================================
// SCROLL TO BOTTOM
// =========================================================

function scrollToBottom() {

    if (!chatBox) {
        return;
    }


    setTimeout(
        function () {

            chatBox.scrollTo({

                top:
                    chatBox.scrollHeight,

                behavior:
                    "smooth"

            });

        },
        50
    );

}


// =========================================================
// LOAD ALL CONVERSATIONS
// =========================================================

async function loadConversations() {

    try {

        const response =
            await fetch(
                "/conversations"
            );


        if (!response.ok) {

            console.error(
                "Unable to load conversations."
            );

            return;

        }


        const conversations =
            await response.json();


        renderConversations(
            conversations
        );


    } catch (error) {

        console.error(
            "Conversation loading error:",
            error
        );

    }

}


// =========================================================
// RENDER CONVERSATIONS
// =========================================================

function renderConversations(
    conversations
) {

    if (!conversationList) {
        return;
    }


    conversationList.innerHTML = "";


    // -----------------------------------------
    // NO CONVERSATIONS
    // -----------------------------------------

    if (
        !Array.isArray(conversations) ||
        conversations.length === 0
    ) {

        conversationList.innerHTML = `

            <div class="conversation-empty">
                No conversations yet.
            </div>

        `;

        return;

    }


    // -----------------------------------------
    // CREATE CONVERSATION ITEMS
    // -----------------------------------------

    conversations.forEach(
        function (conversation) {

            const item =
                document.createElement("div");


            item.className =
                "conversation-item";


            // ---------------------------------
            // ACTIVE CONVERSATION
            // ---------------------------------

            if (
                currentConversationId !== null &&
                Number(conversation.id) ===
                Number(currentConversationId)
            ) {

                item.classList.add(
                    "active"
                );

            }


            // ---------------------------------
            // HTML
            // ---------------------------------

            item.innerHTML = `

                <div class="conversation-main">

                    <span class="conversation-icon">
                        💬
                    </span>

                    <span class="conversation-name">
                        ${escapeHTML(
                            conversation.title
                        )}
                    </span>

                </div>

                <div class="conversation-actions">

                    <button
                        type="button"
                        class="conversation-menu-button"
                        title="More options"
                        aria-label="More options"
                    >
                        ⋮
                    </button>

                    <div class="conversation-menu">

                        <button
                            type="button"
                            class="conversation-action rename-action"
                        >
                            <span>✏️</span>
                            <span>Rename</span>
                        </button>

                        <button
                            type="button"
                            class="conversation-action delete-action"
                        >
                            <span>🗑️</span>
                            <span>Delete</span>
                        </button>

                    </div>

                </div>

            `;


            // ---------------------------------
            // OPEN CONVERSATION
            // ---------------------------------

            const conversationMain =
                item.querySelector(
                    ".conversation-main"
                );


            conversationMain.addEventListener(
                "click",
                function () {

                    loadConversation(
                        conversation.id
                    );

                }
            );


            // ---------------------------------
            // THREE DOT BUTTON
            // ---------------------------------

            const menuButton =
                item.querySelector(
                    ".conversation-menu-button"
                );


            const menu =
                item.querySelector(
                    ".conversation-menu"
                );


            menuButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();


                    // Close other menus
                    document
                        .querySelectorAll(
                            ".conversation-menu.show"
                        )
                        .forEach(
                            function (openMenu) {

                                if (
                                    openMenu !== menu
                                ) {

                                    openMenu.classList.remove(
                                        "show"
                                    );

                                }

                            }
                        );


                    menu.classList.toggle(
                        "show"
                    );

                }
            );


            // ---------------------------------
            // RENAME
            // ---------------------------------

            const renameButton =
                item.querySelector(
                    ".rename-action"
                );


            renameButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();


                    menu.classList.remove(
                        "show"
                    );


                    renameConversation(
                        conversation.id,
                        conversation.title
                    );

                }
            );


            // ---------------------------------
            // DELETE
            // ---------------------------------

            const deleteButton =
                item.querySelector(
                    ".delete-action"
                );


            deleteButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();


                    menu.classList.remove(
                        "show"
                    );


                    deleteConversation(
                        conversation.id
                    );

                }
            );


            conversationList.appendChild(
                item
            );

        }
    );

}


// =========================================================
// RENAME CONVERSATION
// =========================================================

async function renameConversation(
    conversationId,
    currentTitle
) {

    const newTitle =
        prompt(
            "Enter a new conversation name:",
            currentTitle
        );


    // User cancelled
    if (
        newTitle === null
    ) {

        return;

    }


    const title =
        newTitle.trim();


    // Empty title
    if (!title) {

        alert(
            "Conversation title cannot be empty."
        );

        return;

    }


    // Maximum title length
    if (
        title.length > 200
    ) {

        alert(
            "Conversation title cannot exceed 200 characters."
        );

        return;

    }


    try {

        const response =
            await fetch(
                `/conversation/${conversationId}`,
                {
                    method: "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        title:
                            title

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.error ||
                "Unable to rename conversation."
            );

            return;

        }


        // -----------------------------------------
        // REFRESH SIDEBAR
        // -----------------------------------------

        await loadConversations();


    } catch (error) {

        console.error(
            "Rename conversation error:",
            error
        );


        alert(
            "Unable to rename conversation."
        );

    }

}


// =========================================================
// DELETE CONVERSATION
// =========================================================

async function deleteConversation(
    conversationId
) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this conversation?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `/conversation/${conversationId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                data.error ||
                "Unable to delete conversation."
            );

            return;

        }


        // -----------------------------------------
        // IF CURRENT CHAT WAS DELETED
        // -----------------------------------------

        if (
            Number(currentConversationId) ===
            Number(conversationId)
        ) {

            currentConversationId =
                null;


            showWelcomeMessage();

        }


        // -----------------------------------------
        // REFRESH SIDEBAR
        // -----------------------------------------

        await loadConversations();


    } catch (error) {

        console.error(
            "Delete conversation error:",
            error
        );


        alert(
            "Unable to delete conversation."
        );

    }

}


// =========================================================
// LOAD SINGLE CONVERSATION
// =========================================================

async function loadConversation(
    conversationId
) {

    try {

        currentConversationId =
            conversationId;


        const response =
            await fetch(
                `/conversation/${conversationId}`
            );


        if (!response.ok) {

            console.error(
                "Unable to load conversation."
            );

            return;

        }


        const conversation =
            await response.json();


        // -----------------------------------------
        // CLEAR CHAT
        // -----------------------------------------

        if (chatBox) {
            chatBox.innerHTML = "";
        }


        // -----------------------------------------
        // LOAD MESSAGES
        // -----------------------------------------

        if (
            conversation.messages &&
            conversation.messages.length > 0
        ) {

            conversation.messages.forEach(
                function (item) {

                    addHistoryUserMessage(
                        item.user_message,
                        item.timestamp
                    );


                    addHistoryBotMessage(
                        item.bot_response,
                        item.timestamp
                    );

                }
            );

        } else {

            showWelcomeMessage();

        }


        // -----------------------------------------
        // REFRESH SIDEBAR
        // -----------------------------------------

        await loadConversations();


        // -----------------------------------------
        // CLOSE MOBILE SIDEBAR
        // -----------------------------------------

        closeSidebar();


        scrollToBottom();


    } catch (error) {

        console.error(
            "Conversation loading error:",
            error
        );

    }

}


// =========================================================
// HISTORY USER MESSAGE
// =========================================================

function addHistoryUserMessage(
    message,
    timestamp
) {

    if (!chatBox) {
        return;
    }


    const row =
        document.createElement("div");


    row.className =
        "message-row user-row";


    row.innerHTML = `

        <div class="message-content">

            <div class="message-sender">
                You
            </div>

            <div class="user-message">

                ${formatMessage(message)}

                <div class="message-time">
                    ${formatHistoryTime(
                        timestamp
                    )}
                </div>

            </div>

        </div>

        <div class="message-avatar user-avatar">
            👤
        </div>

    `;


    chatBox.appendChild(row);

}


// =========================================================
// HISTORY BOT MESSAGE
// =========================================================

function addHistoryBotMessage(
    message,
    timestamp
) {

    if (!chatBox) {
        return;
    }


    const row =
        document.createElement("div");


    row.className =
        "message-row bot-row";


    row.innerHTML = `

        <div class="message-avatar bot-avatar">
            🤖
        </div>

        <div class="message-content">

            <div class="message-sender">
                ChatNova
            </div>

            <div class="bot-message">

                ${formatMessage(message)}

                <div class="message-time">
                    ${formatHistoryTime(
                        timestamp
                    )}
                </div>

            </div>

        </div>

    `;


    chatBox.appendChild(row);

}


// =========================================================
// WELCOME MESSAGE
// =========================================================

function showWelcomeMessage() {

    if (!chatBox) {
        return;
    }


    chatBox.innerHTML = `

        <div class="message-row bot-row">

            <div class="message-avatar bot-avatar">
                🤖
            </div>

            <div class="message-content">

                <div class="message-sender">
                    ChatNova
                </div>

                <div class="bot-message">

                    Hello! 👋

                    <br><br>

                    I'm <strong>ChatNova</strong>,
                    your intelligent conversation partner.

                    <br><br>

                    How can I help you today?

                    <div class="message-time">
                        Just now
                    </div>

                </div>

            </div>

        </div>

    `;

}


// =========================================================
// NEW CHAT
// =========================================================

if (newChatButton) {

    newChatButton.addEventListener(
        "click",
        async function () {

            currentConversationId =
                null;


            showWelcomeMessage();


            if (messageInput) {

                messageInput.value = "";

                messageInput.style.height =
                    "auto";

                messageInput.focus();

            }


            await loadConversations();


            closeSidebar();

        }
    );

}


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");


    div.textContent =
        text || "";


    return div.innerHTML;

}


// =========================================================
// SIDEBAR
// =========================================================

const sidebar =
    document.getElementById(
        "chatSidebar"
    );


const sidebarToggle =
    document.getElementById(
        "sidebarToggle"
    );


const sidebarClose =
    document.getElementById(
        "sidebarClose"
    );


const sidebarOverlay =
    document.getElementById(
        "sidebarOverlay"
    );


// =========================================================
// OPEN SIDEBAR
// =========================================================

function openSidebar() {

    if (!sidebar) {
        return;
    }


    sidebar.classList.add(
        "open"
    );


    if (sidebarOverlay) {

        sidebarOverlay.classList.add(
            "active"
        );

    }

}


// =========================================================
// CLOSE SIDEBAR
// =========================================================

function closeSidebar() {

    if (!sidebar) {
        return;
    }


    sidebar.classList.remove(
        "open"
    );


    if (sidebarOverlay) {

        sidebarOverlay.classList.remove(
            "active"
        );

    }

}


// =========================================================
// SIDEBAR TOGGLE
// =========================================================

if (sidebarToggle) {

    sidebarToggle.addEventListener(
        "click",
        openSidebar
    );

}


if (sidebarClose) {

    sidebarClose.addEventListener(
        "click",
        closeSidebar
    );

}


if (sidebarOverlay) {

    sidebarOverlay.addEventListener(
        "click",
        closeSidebar
    );

}


// =========================================================
// CLOSE OPEN MENUS WHEN CLICKING OUTSIDE
// =========================================================

document.addEventListener(
    "click",
    function () {

        document
            .querySelectorAll(
                ".conversation-menu.show"
            )
            .forEach(
                function (menu) {

                    menu.classList.remove(
                        "show"
                    );

                }
            );

    }
);


// =========================================================
// INITIALIZE CHATNOVA
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadConversations();


        if (messageInput) {

            messageInput.focus();

        }

    }
);