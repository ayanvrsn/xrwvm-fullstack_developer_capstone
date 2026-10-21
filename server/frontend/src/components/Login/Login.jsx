import React,{useState,useEffect} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Login(){
 const [userName,setUserName]=useState(''),[password,setPassword]=useState(''),[error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/session').catch(()=>{});},[]);
 async function submit(e){e.preventDefault();try{const r=await api('/djangoapp/login',{method:'POST',body:JSON.stringify({userName,password})});sessionStorage.setItem('username',r.userName);sessionStorage.setItem('firstname',r.firstName);sessionStorage.setItem('lastname',r.lastName);window.location.href='/';}catch(e){setError(e.message);}}
 return <><Header/><main className="container py-5"><h1>Login</h1><form style={{maxWidth:480}} onSubmit={submit}><label className="d-block my-3">Username<input className="form-control" required value={userName} onChange={e=>setUserName(e.target.value)}/></label><label className="d-block my-3">Password<input className="form-control" type="password" required value={password} onChange={e=>setPassword(e.target.value)}/></label><p role="alert">{error}</p><button className="btn btn-primary">Login</button> <a href="/register">Register Now</a></form></main></>;
}
