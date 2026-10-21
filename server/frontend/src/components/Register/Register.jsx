import React,{useState,useEffect} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Register(){
 const [data,setData]=useState({userName:'',firstName:'',lastName:'',email:'',password:''});
 const [error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/session').catch(()=>{});},[]);
 async function submit(e){e.preventDefault();try{const r=await api('/djangoapp/register',{method:'POST',body:JSON.stringify(data)});sessionStorage.setItem('username',r.userName);window.location.href='/';}catch(e){setError(e.message);}}
 return <><Header/><main className="container py-5"><h1>Sign Up</h1><p>Create your Best Cars account to post dealership reviews.</p><form onSubmit={submit} style={{maxWidth:480}}>{[['userName','Username','text'],['firstName','First name','text'],['lastName','Last name','text'],['email','Email','email'],['password','Password','password']].map(([key,label,type])=><label className="d-block my-3" key={key}>{label}<input className="form-control" required type={type} minLength={key==='password'?8:1} value={data[key]} onChange={e=>setData({...data,[key]:e.target.value})}/></label>)}<p role="alert">{error}</p><button className="btn btn-primary">Register</button></form></main></>;
}
