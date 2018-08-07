import React, {Component} from "react";
import {Upload, message, Button, Icon, Modal, Input, Radio, Form} from "antd";

const RadioGroup = Radio.Group;
const FormItem = Form.Item;


const NewRazaForm = Form.create() (
    class extends React.Component {

        state = {
            other_raza: false
        };

        handleChoices = (e) => {
            console.log("CHANGE RADIO BUTTON", e);
            if(e.target.value === this.props.dogs.length){
                this.setState({
                    other_raza: true,
                }, () => {
                    this.props.form.validateFields(['text_raza'], { force: true });
                });
            }else{
                this.setState({
                    other_raza: false,
                }, () => {
                    this.props.form.validateFields(['text_raza'], { force: true });
                });
            }
        };

        render(){
            const radioStyle = {
                display: 'block',
                height: '30px',
                lineHeight: '30px',
            };
            const { visible, onCancel, onCreate, form, dogs } = this.props;
            const { getFieldDecorator } = form;
            return (<Modal
                title="Basic Modal"
                visible={visible}
                onOk={onCreate}
                onCancel={onCancel}>
                <p>No puedo reconocer bien este objeto. ¿Que es?</p>
                <Form layout="vertical">
                    <FormItem label="¿Algunas de estas opciones?">
                        {getFieldDecorator('choice_raza', {
                            rules: [{ required: true, message: 'Selecciona una raza' }],
                        })(
                            <RadioGroup value={this.state.choice_raza} onChange={this.handleChoices}>
                                {dogs.map((dog, i) => <Radio style={radioStyle} value={i}>{dog.label}</Radio>)}
                                <Radio style={radioStyle} value={dogs.length}>Ninguna de las anteriores</Radio>
                            </RadioGroup>
                        )}
                    </FormItem>
                    <FormItem label="¿No es ninguna de las anteriores? ¿Cual es?">
                        {getFieldDecorator('text_raza', {
                            rules: [
                                {
                                    required: this.state.other_raza,
                                    message: 'Sino es ninguna de las opciones anteriores, por favor describa cual es.'
                                }
                            ],
                        })(
                            <Input placeholder="Escriba que es" />
                        )}
                    </FormItem>
                </Form>
            </Modal>);
        }
    }
);




class PageFormImage extends Component {


    onUploadImage = (info) => {
        if (info.file.status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            let probability = info.file.response.predictions[0].probability.toFixed(2)*100;
            if (probability > 55){
                message.success(`Hay un ${probability} % de probabilidades que sea un ${info.file.response.predictions[0].label}`);
            }else{
                this.setState({
                    visible: true,
                    options_know_dogs: info.file.response.predictions
                });
            }
        } else if (info.file.status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
        console.log(info);
    };

    upload_props = {
        name: 'image',
        accept: 'image/*',
        multiple: false,
        action: 'http://0.0.0.0:8000/predict/',
        headers: {
            authorization: 'authorization-text',
        },
        onChange: this.onUploadImage,
    };

    state = {
        visible: false,
        options_know_dogs: [],
        choice_dog: null,
        dog_name: null
    };

    handleOk = () => {
        const form = this.formRef.props.form;
        form.validateFields((err, values) => {
            if (err) {
                return;
            }

            console.log('Received values of form: ', values);
            form.resetFields();
            this.setState({ visible: false });
        });
    };


    handleCancel = (e) => {
        const form = this.formRef.props.form;
        form.resetFields();
        this.setState({
            visible: false,
        });
    };

    onSelectDog = (e) => {
        console.log('radio checked', e.target.value);
        this.setState({
            value: e.target.value,
        });
    };

    saveFormRef = (formRef) => {
        this.formRef = formRef;
    };

    render() {

        return (
            <div>
                <NewRazaForm
                    wrappedComponentRef={this.saveFormRef}
                    visible={this.state.visible}
                    dogs={this.state.options_know_dogs}
                    onCancel={this.handleCancel}
                    onCreate={this.handleOk}
                />
                <div>
                    <Upload {...this.upload_props}>
                        <Button><Icon type="upload" /> Click to Upload</Button>
                    </Upload>
                </div>
            </div>
        );
    }
}

export default PageFormImage;
