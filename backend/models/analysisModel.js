import mongoose from 'mongoose';

const analysisSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
    },
    datasetId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Dataset',
      required: [true, 'Dataset ID is required'],
    },
    forecast: {
      type: String,
      default: '',
    },
    sentiment: {
      type: String,
      default: '',
    },
    businessInsights: {
      type: String,
      default: '',
    },
    marketingRecommendations: {
      type: String,
      default: '',
    },
    analysisStatus: {
      type: String,
      enum: ['processing', 'completed', 'failed'],
      default: 'processing',
    },
  },
  {
    timestamps: true, // Automatically manages createdAt and updatedAt fields
  }
);

const Analysis = mongoose.model('Analysis', analysisSchema);

export default Analysis;
