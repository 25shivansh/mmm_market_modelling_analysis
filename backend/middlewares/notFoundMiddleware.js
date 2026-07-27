export function notFound(req, res, next) {
    return res.status(404).json({
        message: `Route not found - ${req.originalUrl}`,
        success: false,
    });
}

export default notFound;
