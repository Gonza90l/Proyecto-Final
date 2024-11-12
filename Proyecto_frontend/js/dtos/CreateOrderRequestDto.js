class CreateOrderRequestDto {
    constructor(user_id, total, status, order_items) {
        this.user_id = user_id;
        this.total = total;
        this.status = status;
        this.order_items = order_items; // This should be a list of OrderHasMenuDTO
    }
}


export default CreateOrderRequestDto;
