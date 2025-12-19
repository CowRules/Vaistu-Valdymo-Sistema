import axios from "axios";
import { useEffect, useState, type FormEvent } from "react";
import { Button, Form } from "react-bootstrap";
import { useNavigate } from "react-router";

export default function LoginPage(){
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    async function handleLogin(e:FormEvent){
        e.preventDefault()
        const status = await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/login", {"username":username, "password":password}, {withCredentials: true})
        if (status.status === 200) navigate("/")
    }
    async function guestLogin() {
        const status = await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/login", {"username":"Guest", "password":"Guest"}, {withCredentials: true})
        if (status.status === 200) navigate("/")
    }
    return(
        <center>
            <div style={{backgroundColor:"gray", borderRadius:'12px', minHeight:'400px', minWidth:'400px', padding:'50px'}}>
                <h1>Login</h1>
                <Form onSubmit={(e)=>handleLogin(e)}>
                    <Form.Group className="mb-4">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Username" onChange={(e)=>setUsername(e.target.value)} value={username}></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-4">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" onChange={(e)=>setPassword(e.target.value)} value={password}></Form.Control>
                    </Form.Group>
                    <Form.Group>
                        <Button variant="primary" type="submit">Login</Button>
                        <Button variant="link" onClick={()=>{guestLogin()}}>Continue as guest</Button>
                    </Form.Group>
                    <Form.Group>
                        Don't have an account? <Button variant="link" onClick={()=>navigate("/register")}>Register</Button>
                    </Form.Group>
                </Form>
            </div>
        </center>
    )
}