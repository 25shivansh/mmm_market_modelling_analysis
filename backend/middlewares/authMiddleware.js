import jwt from 'jsonwebtoken';

export function protect(req, res, next) {
    try {
        const authHeader = req.headers.authorization;

        // Check if Authorization header exists and starts with "Bearer "
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({
                message: "Access denied. No token provided.",
                success: false,
            });
        }

        // Extract token from "Bearer <token>"
        const token = authHeader.split(' ')[1];

        if (!token) {
            return res.status(401).json({
                message: "Access denied. Token is missing.",
                success: false,
            });
        }

        // Verify token using JWT secret
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        // Store decoded payload (e.g. { id: user._id }) inside req.user
        req.user = decoded;

        // Proceed to next middleware or route controller
        next();

    } catch (err) {
        return res.status(401).json({
            message: "Invalid or expired token.",
            success: false,
        });
    }
}
