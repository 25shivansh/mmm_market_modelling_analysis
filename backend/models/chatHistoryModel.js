import mongoose from 'mongoose';

const chatHistorySchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
    },
    datasetId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Dataset',
    },
    message: {
      type: String,
      trim: true,
    },
    response: {
      type: String,
      default: 'AI response will be added later',
    },
    question: {
      type: String,
      trim: true,
    },
    answer: {
      type: String,
    },
  },
  {
    timestamps: true, // Automatically creates createdAt and updatedAt fields
  }
);

const ChatHistory = mongoose.model('ChatHistory', chatHistorySchema);

export default ChatHistory;
