import axios from "axios";
import { useEffect, useState, type FormEvent } from "react";
import { Button, Form } from "react-bootstrap";
import { useNavigate } from "react-router";

export default function RegisterPage(){
    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")
    async function handleLogin(e:FormEvent){
        e.preventDefault()
        const status = await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/register", 
            {"username":username, "password":password, "email":email, "is_administrator":false, "role":"client"}, {withCredentials: true})
        if (status.status === 201) navigate("/login")
    }
    return(
        <center>
            <div style={{backgroundColor:"gray", borderRadius:'12px', minHeight:'400px', minWidth:'400px', padding:'50px'}}>
                <h1>Register</h1>
                <Form onSubmit={(e)=>handleLogin(e)}>
                    <Form.Group className="mb-4">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text" placeholder="Username" onChange={(e)=>setUsername(e.target.value)} value={username}></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-4">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder="example@gmail.com" onChange={(e)=>setEmail(e.target.value)} value={email}></Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-4">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password" onChange={(e)=>setPassword(e.target.value)} value={password}></Form.Control>
                    </Form.Group>
                    <Button variant="primary" type="submit">Register</Button>
                </Form>
            </div>
        </center>
    )
}