import axios from "axios";
import { Button, Container } from "react-bootstrap";
import { useNavigate } from "react-router";
import NavBar from "../components/NavBar";

export default function HomePage() {
    const navigate = useNavigate()
    async function handleLogout() {
        const res = await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/logout", {}, {withCredentials:true})
        if (res.status === 200) {
            navigate("/login")
        }
    }
    return (
        <>
        <NavBar/>
            <Container>
            </Container>
        </>
    )
}