import ChatHistory from '../models/chatHistoryModel.js';

// Send a message to the AI assistant
export async function sendMessage(req, res) {
    try {
        const { message, datasetId } = req.body;

        if (!message || !message.trim()) {
            return res.status(400).json({
                success: false,
                message: "Message is required",
            });
        }

        const chat = await ChatHistory.create({
            userId: req.user.id,
            datasetId: datasetId || null,
            message: message.trim(),
            response: "AI response will be added later",
        });

        return res.status(201).json({
            success: true,
            message: "Message sent successfully",
            chat,
        });

    } catch (err) {
        return res.status(500).json({
            success: false,
            message: err.message,
        });
    }
}

// Get chat history for the logged-in user
export async function getChatHistory(req, res) {
    try {
        const filter = { userId: req.user.id };
        if (req.params.datasetId) {
            filter.datasetId = req.params.datasetId;
        }

        const chats = await ChatHistory.find(filter).sort({ createdAt: -1 });

        return res.status(200).json({
            success: true,
            message: "Chat history fetched successfully",
            count: chats.length,
            chats,
        });

    } catch (err) {
        return res.status(500).json({
            success: false,
            message: err.message,
        });
    }
}

// Clear chat history for the logged-in user
export async function clearChatHistory(req, res) {
    try {
        const filter = { userId: req.user.id };
        if (req.params.datasetId) {
            filter.datasetId = req.params.datasetId;
        }

        await ChatHistory.deleteMany(filter);

        return res.status(200).json({
            success: true,
            message: "Chat history cleared successfully",
        });

    } catch (err) {
        return res.status(500).json({
            success: false,
            message: err.message,
        });
    }
}
