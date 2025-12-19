import axios from "axios"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router"
import type { Reserves } from "../types/types"
import { Button, Col, Form, Modal, Row, Table } from "react-bootstrap"
import NavBar from "../components/NavBar"

export default function ReserveListPage(){
    const navigate = useNavigate()
    const [reserves, setReserves] = useState<Reserves[]>([])
    const [show, setShow] = useState(false);
    const [reserveName, setReserveName] = useState("")

    const handleClose = () => {setShow(false); setReserveName("")};
    const handleShow = () => setShow(true);
    async function fetchReserves() {
        try {
            let res = await axios.get("https://vaistu-valdymo-sistema.onrender.com/api/reserves", {withCredentials: true})
            setReserves(res.data)
        } catch (error) {
            try {
                await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/refresh/", {}, {withCredentials: true})
                let res = await axios.get("https://vaistu-valdymo-sistema.onrender.com/api/reserves", {withCredentials: true})
                setReserves(res.data)
            } catch (error) {
                navigate("/login")
            }
        }
    }
    async function addReserve(){
        if(!reserveName) return
        try {
            await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/reserve/create", {"name":reserveName}, {withCredentials: true})
            handleClose()
            fetchReserves()
        } catch (error) {
            try {
                await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/refresh/", {}, {withCredentials: true})
                await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/reserve/create", {"name":reserveName}, {withCredentials: true})
                handleClose()
                fetchReserves()
            } catch (error) {
                handleClose()
                navigate("/login")
            }
        }
    }
    async function deleteReserve(id:string){
        try {
            await axios.delete(`https://vaistu-valdymo-sistema.onrender.com/api/reserve/delete/${id}`, {withCredentials: true})
            fetchReserves()
        } catch (error) {
            try {
                await axios.post("https://vaistu-valdymo-sistema.onrender.com/api/refresh/", {}, {withCredentials: true})
                await axios.delete(`https://vaistu-valdymo-sistema.onrender.com/api/reserve/delete/${id}`, {withCredentials: true})
                fetchReserves()
            } catch (error) {
                console.log(error)
            }
        }
    }
    useEffect(()=>{
        fetchReserves()
    },[])
    return(
        <>
            <NavBar/>
            <Row>
                <Col>
                    <h1>Reserves</h1>
                </Col>
                <Col>
                    <Button variant="primary" onClick={()=>{handleShow()}} style={{marginLeft: 10}} className="my-auto">New</Button>
                </Col>
            </Row>
            
            <Table striped bordered hover size="lg">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Reserve name</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {reserves.map((reserve)=>(
                        <tr key={reserve.id}>
                            <td onClick={()=>navigate(`/reserve/${reserve.id}`)}>{reserve.id}</td>
                            <td onClick={()=>navigate(`/reserve/${reserve.id}`)}>{reserve.name}</td>
                            <td onClick={()=>deleteReserve(reserve.id)} className="p-0">
                                <Button className="w-100 h-100 rounded-0" variant="outline-danger" onClick={()=>deleteReserve(reserve.id)}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                    </svg>
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add new reserve</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3" >
                            <Form.Label>Reserve name</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Reserve name"
                                autoFocus
                                onChange={(e)=>setReserveName(e.target.value)}
                                value={reserveName}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={()=>addReserve()}>
                        Add
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}