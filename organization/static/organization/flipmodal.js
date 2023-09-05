class Modal {
    constructor(modalButton) {
        this.element = modalButton;
        this.modalID = modalButton.dataset.id;
        this.modalNode = document.querySelector(`#${this.modalID}`);
        this.modalParent = this.modalNode.parentNode;
        this.open = false;

        this.modalInit();
    }

    modalInit = () => {
        this.element.addEventListener('click', this.openModal);
        this.modalParent.addEventListener('mousedown', this.handleOverlayClick);

        let closeButtons = this.modalNode.querySelectorAll('.modal-close');
        closeButtons.forEach(cur => cur.addEventListener('click', this.closeModal))
    }

    openModal = () => {
        this.modalParent.classList.add('modal-background--active');

        this.modalNode.classList.add('modal--active');

        this.open = !this.open;
    }

    closeModal = () => {
        this.modalParent.classList.remove('modal-background--active');

        this.modalNode.classList.remove('modal--active');

        this.open = !this.open;
    }

    handleOverlayClick = (e) => {
        if (!e.target.closest('.modal')) {
            this.closeModal();
        }
    }
}

let buttons = document.querySelectorAll('.flip-modal-button');
buttons.forEach(cur => new Modal(cur));