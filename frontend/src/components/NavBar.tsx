import axios from "axios";
import { useEffect, useState } from "react";
import { Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import { useNavigate } from "react-router";

export default function NavBar(){
    const [username, setUsername] = useState("");
    const [role, setRole] = useState("");
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()
    useEffect(()=>{
        async function fetchUser() {
            try {
                let res = await axios.get("https://vaistu-valdymo-sistema.onrender.com/api/profile", {withCredentials: true})
                setUsername(res.data['username'])
                setRole(res.data["role"])
                setLoading(false)
            } catch (error) {
                try {
                    await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/refresh/", {}, {withCredentials: true})
                    let res = await axios.get("https://vaistu-valdymo-sistema.onrender.com/api/profile", {withCredentials: true})
                    setUsername(res.data['username'])
                    setRole(res.data["role"])
                    setLoading(false)
                } catch (error) {
                    navigate("/login")
                }
            }
        }
        fetchUser()
    })
    async function handleLogout() {
        const res = await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/logout", {}, {withCredentials:true})
        if (res.status === 200) {
            navigate("/login")
        }
    }
    return(
        <>
            {!loading && <Navbar expand="sm" className="bg-body-tertiary fixed-top">
                <Container>
                    <Navbar.Brand href="/">VVS</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="justify-content-start">
                            {(role==="admin"||role==="client") &&<Nav.Link href="/reserves">Reserves</Nav.Link>}
                            <Nav.Link href="/medicine">Medicine</Nav.Link>
                            {role==="admin" && <Nav.Link href="/pending_medicine">Pending medicine</Nav.Link>}
                            <NavDropdown title={username} id="basic-nav-dropdown" className="ms-auto">
                                {(role==="admin"||role==="client") &&<NavDropdown.Item href="/profile">Profile</NavDropdown.Item>}
                                <NavDropdown.Item onClick={handleLogout}>
                                    Log out
                                </NavDropdown.Item>
                            </NavDropdown>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>}
        </>
    )
}