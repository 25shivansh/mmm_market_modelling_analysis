import Dataset from '../models/datasetModel.js';

// Upload a new dataset
export async function uploadDataset(req, res) {
    try {
        // Check if file was uploaded
        if (!req.file) {
            return res.status(400).json({
                success: false,
                message: "Please upload a CSV file",
            });
        }

        // Extract optional metadata from req.body
        const { datasetName, description } = req.body;

        // Save dataset in MongoDB
        const dataset = await Dataset.create({
            userId: req.user.id,
            datasetName: datasetName || req.file.originalname,
            description: description || '',
            filename: req.file.filename,
            originalFilename: req.file.originalname,
            filePath: req.file.path,
            fileSize: req.file.size,
            fileType: req.file.mimetype,
        });

        return res.status(201).json({
            success: true,
            message: "Dataset uploaded successfully",
            dataset: dataset,
        });

    } catch (err) {
        return res.status(500).json({
            success: false,
            message: err.message,
        });
    }
}

// Get all datasets for the logged-in user
export async function getAllDatasets(req, res) {
    try {
        const datasets = await Dataset.find({ userId: req.user.id }).sort({ createdAt: -1 });

        return res.status(200).json({
            message: "Datasets fetched successfully",
            success: true,
            count: datasets.length,
            datasets,
        });

    } catch (err) {
        return res.status(500).json({
            message: err.message,
            success: false,
        });
    }
}

// Get a single dataset by ID for the logged-in user
export async function getDatasetById(req, res) {
    try {
        const dataset = await Dataset.findOne({
            _id: req.params.id,
            userId: req.user.id,
        });

        if (!dataset) {
            return res.status(404).json({
                message: "Dataset not found",
                success: false,
            });
        }

        return res.status(200).json({
            message: "Dataset fetched successfully",
            success: true,
            dataset,
        });

    } catch (err) {
        return res.status(500).json({
            message: err.message,
            success: false,
        });
    }
}

// Delete a dataset by ID for the logged-in user
export async function deleteDataset(req, res) {
    try {
        const deletedDataset = await Dataset.findOneAndDelete({
            _id: req.params.id,
            userId: req.user.id,
        });

        if (!deletedDataset) {
            return res.status(404).json({
                message: "Dataset not found",
                success: false,
            });
        }

        return res.status(200).json({
            message: "Dataset deleted successfully",
            success: true,
        });

    } catch (err) {
        return res.status(500).json({
            message: err.message,
            success: false,
        });
    }
}
