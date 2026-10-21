const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const Reviews = require('./review');
const Dealers = require('./dealership');
const app = express();
app.use(cors());
app.use(express.json({limit:'32kb'}));
const handle = fn => (req,res,next) => Promise.resolve(fn(req,res,next)).catch(next);
app.get('/', (req,res) => res.send('Welcome to the Mongoose API'));
app.get('/fetchReviews',handle(async(req,res)=>res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id',handle(async(req,res)=>res.json(await Reviews.find({dealership:Number(req.params.id)}).lean())));
app.get('/fetchDealers',handle(async(req,res)=>res.json(await Dealers.find().sort({id:1}).lean())));
app.get('/fetchDealers/:state',handle(async(req,res)=>res.json(await Dealers.find({state:req.params.state}).sort({id:1}).lean())));
app.get('/fetchDealer/:id',handle(async(req,res)=>res.json(await Dealers.find({id:Number(req.params.id)}).lean())));
app.post('/insert_review',handle(async(req,res)=>{
  const data=req.body;
  if(!Number.isInteger(Number(data.dealership)) || !String(data.review||'').trim()) return res.status(400).json({error:'Invalid review'});
  if(!await Dealers.exists({id:Number(data.dealership)})) return res.status(404).json({error:'Dealer not found'});
  // Atomic counter avoids duplicate IDs when requests arrive concurrently.
  const counter=await mongoose.connection.collection('counters').findOneAndUpdate(
    {_id:'review_id'},{$inc:{value:1}},{upsert:true,returnDocument:'after'});
  const created=await Reviews.create({...data,id:counter.value});
  res.status(201).json(created);
}));
app.use((error,req,res,next)=>{
  console.error(error.message);
  res.status(error.name==='ValidationError'?400:500).json({error:'Request could not be completed'});
});
async function start(){
  await mongoose.connect(process.env.MONGO_URL||'mongodb://mongo_db:27017/dealershipsDB');
  const dealerData=JSON.parse(fs.readFileSync(path.join(__dirname,'data/dealerships.json'),'utf8')).dealerships;
  const reviewData=JSON.parse(fs.readFileSync(path.join(__dirname,'data/reviews.json'),'utf8')).reviews;
  if(await Dealers.estimatedDocumentCount()===0) await Dealers.insertMany(dealerData);
  if(await Reviews.estimatedDocumentCount()===0) await Reviews.insertMany(reviewData);
  const last=await Reviews.findOne().sort({id:-1});
  await mongoose.connection.collection('counters').updateOne({_id:'review_id'},{$max:{value:last?last.id:0}},{upsert:true});
  app.listen(process.env.PORT||3030,()=>console.log('Mongoose API ready on port '+(process.env.PORT||3030)));
}
if(require.main===module) start().catch(error=>{console.error(error);process.exit(1);});
module.exports={app,start};
