import { useState } from "react";
import { registerUser } from "../api/authApi";

function Register() {
  const [form, setForm] = useState({});

  const submit = async (e) => {
    e.preventDefault();
    await registerUser(form);
    alert("Registered");
  };

  return (
    <form onSubmit={submit}>
      <h2>Register</h2>
      <input placeholder="Name" onChange={e => setForm({...form, name:e.target.value})} />
      <input placeholder="Email" onChange={e => setForm({...form, email:e.target.value})} />
      <input placeholder="Password" type="password" onChange={e => setForm({...form, password:e.target.value})} />
      <input placeholder="Role" onChange={e => setForm({...form, role:e.target.value})} />
      <input placeholder="Constituency ID" onChange={e => setForm({...form, constituency_id:e.target.value})} />
      <button>Register</button>
    </form>
  );
}

export default Register;
