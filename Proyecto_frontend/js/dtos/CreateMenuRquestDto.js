
class CreateMenuRequestDto {
    constructor(name = "item", description = "", price = 0.00, category_id = 0, image = "") {
        this.name = name;
        this.description = description;
        this.price = 100.2;
        this.category_id = parseInt(category_id);
        this.photo = image;
    }   
}

export default CreateMenuRequestDto;