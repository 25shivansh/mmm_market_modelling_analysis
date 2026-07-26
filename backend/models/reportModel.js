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
    },
    title: {
      type: String,
      required: [true, 'Report title is required'],
      trim: true,
    },
    content: {
      type: String,
      default: '',
    },
    status: {
      type: String,
      enum: ['pending', 'generated', 'failed'],
      default: 'pending',
    },
    generatedAt: {
      type: Date,
    },
  },
  {
    timestamps: true, // Automatically creates createdAt and updatedAt fields
  }
);

const Report = mongoose.model('Report', reportSchema);

export default Report;
