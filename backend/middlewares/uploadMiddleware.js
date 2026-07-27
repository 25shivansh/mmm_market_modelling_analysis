import multer from 'multer';
import path from 'path';
import fs from 'fs';

// Ensure the uploads folder exists
const uploadDir = 'uploads/';
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Configure Multer storage destination and custom filename
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const uniquePrefix = Date.now();
        const extension = path.extname(file.originalname);
        cb(null, `${uniquePrefix}-${file.originalname}`);
    },
});

// File filter to restrict uploads to CSV files only
const fileFilter = (req, file, cb) => {
    const fileExtension = path.extname(file.originalname).toLowerCase();
    const isCsvMime = file.mimetype === 'text/csv' || file.mimetype === 'application/vnd.ms-excel';

    if (fileExtension === '.csv' || isCsvMime) {
        cb(null, true);
    } else {
        cb(new Error('Only CSV files are allowed!'), false);
    }
};

// Configure Multer upload middleware
const upload = multer({
    storage,
    fileFilter,
});

export default upload;
