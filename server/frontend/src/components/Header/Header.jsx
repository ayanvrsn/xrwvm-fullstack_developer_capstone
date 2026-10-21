import React,{useEffect,useState} from 'react';
import {api} from '../../api';
import '../assets/bootstrap.min.css';
export default function Header(){
 const [user,setUser]=useState(null);
 useEffect(()=>{api('/djangoapp/session').then(d=>setUser(d.userName)).catch(()=>setUser(null));},[]);
 async function logout(e){e.preventDefault();try{await api('/djangoapp/logout',{method:'POST'});sessionStorage.clear();alert('Logging out '+user+'...');window.location.href='/';}catch(e){alert(e.message);}}
 return <nav className="navbar navbar-expand navbar-light p-4" style={{background:'darkturquoise'}}><h2 className="me-4">Best Cars Dealerships</h2><a className="nav-link" href="/">Home</a><a className="nav-link" href="/about/">About Us</a><a className="nav-link" href="/contact/">Contact Us</a><div className="ms-auto">{user?<><strong>{user}</strong> <a href="/" onClick={logout}>Logout</a></>:<><a href="/login">Login</a> | <a href="/register">Register</a></>}</div></nav>;
}
