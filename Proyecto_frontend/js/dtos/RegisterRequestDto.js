//RegisterRequestDTO
//Clase que representa un request de registro
class RegisterRequestDTO {
    constructor(name, lastname, email, password) {
        this.name = name;
        this.lastname = lastname
        this.email = email;
        this.password = password;
    }
}

export default RegisterRequestDTO;

