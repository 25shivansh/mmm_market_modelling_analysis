import mongoose from 'mongoose';

const reportSchema = new mongoose.Schema(
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
    reportType: {
      type: String,
      required: [true, 'Report type is required'],
      enum: ['forecast', 'sentiment', 'marketing', 'business_insights', 'summary'],
      default: 'summary',
    },
    title: {
      type: String,
      required: [true, 'Report title is required'],
      trim: true,
      default: 'Data Understanding Report',
    },
    content: {
      type: String,
      default: '',
    },
    reportContent: {
      type: String,
      default: '',
    },
    summary: {
      type: Object,
      default: {},
    },
    status: {
      type: String,
      enum: ['pending', 'generated', 'completed', 'failed'],
      default: 'completed',
    },
    generatedAt: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true, // Automatically creates createdAt and updatedAt fields
  }
);

const Report = mongoose.model('Report', reportSchema);

export default Report;
