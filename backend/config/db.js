import mongoose from 'mongoose'
const connectDB =async ()=>{
    try{
        const conn =await mongoose.connect(process.env.MONGODB_URL);
        console.log("MongoDB connected successfully")
    }catch(err){
        console.log("Database connection failed",err.message);
        process.exit(1);

    }

}
export default connectDB