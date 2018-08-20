import React, {Component} from "react";
import {Upload, message, Button, Icon, Modal, Input, Radio, Form} from "antd";

const RadioGroup = Radio.Group;
const FormItem = Form.Item;


const PredictionForm = Form.create() (
    class extends React.Component {

        constructor(props) {
            super(props);
            this.state = {
                other_obj: false
            };
            this.handleChoiceSuccessPredChange = this.handleChoiceSuccessPredChange.bind(this);
        }

        handleChoiceSuccessPredChange(e) {
            this.props.handleChoiceSuccessPredChange(!!e.target.value);
        }

        getPredictions = () => {
            return this.props.prediction !== null ? this.props.prediction['predictions'] : [];
        };

        handleChoices = (e) => {
            const possible_predictions =  this.getPredictions();
            this.setState({
                other_obj: e.target.value === possible_predictions.length,
            }, () => {
                this.props.form.validateFields(['text_obj'], { force: true });
            });
        };

        render(){
            const radioStyle = {
                display: 'block',
                height: '30px',
                lineHeight: '30px',
            };
            const { visible, onCancel, onCreate, form, success_prediction } = this.props;
            const possible_predictions =  this.getPredictions();
            const { getFieldDecorator } = form;

            let header_pred = '';
            let field_feedback = '';

            if(possible_predictions.length > 0){
                let pred = possible_predictions[0];
                let probability = pred.probability*100;

                if(probability > 55){
                    header_pred =  (
                        <React.Fragment>
                            <h3>There're {probability.toFixed(2)} % to probabilities that is a/an {pred.label}</h3>
                            <FormItem label="¿Is true?">
                                {getFieldDecorator('success_prediction', {
                                    rules: [{ required: true, message: 'This field is required.' }],
                                    setFieldsValue: success_prediction ? 1 : 0,
                                    initialValue: null
                                })(
                                    <RadioGroup onChange={this.handleChoiceSuccessPredChange}>
                                        <Radio style={radioStyle} value={1}>Yes</Radio>
                                        <Radio style={radioStyle} value={0}>No</Radio>
                                    </RadioGroup>
                                )}
                            </FormItem>
                        </React.Fragment>
                    );
                }

                if(success_prediction === false || probability < 55){
                    field_feedback = (
                        <React.Fragment>
                            <h3>I can't recognize this object. ¿Can you help me?</h3>
                            <FormItem label="¿Any these options?">
                                {getFieldDecorator('choice_obj', {
                                    rules: [{ required: true, message: 'Select one option' }],
                                    setFieldsValue: this.state.choice_obj,
                                    initialValue: null
                                })(
                                    <RadioGroup onChange={this.handleChoices}>
                                        {possible_predictions.map((pred, i) => <Radio style={radioStyle} key={`pred_${i}`} value={i}>{pred.label}</Radio>)}
                                        <Radio style={radioStyle} value={possible_predictions.length}>Ninguna de las anteriores</Radio>
                                    </RadioGroup>
                                )}
                            </FormItem>
                            <FormItem label="Is not none of the above options? Can you describe it?">
                                {getFieldDecorator('text_obj', {
                                    rules: [
                                        {
                                            required: this.state.other_obj,
                                            message: 'If not none of the above optiones. Please, describe it.'
                                        }
                                    ],
                                })(
                                    <Input placeholder="What is it?" />
                                )}
                            </FormItem>
                        </React.Fragment>
                    )
                }
            }

            return (<Modal
                title="Prediction"
                visible={visible}
                onOk={onCreate}
                onCancel={onCancel}
                destroyOnClose={true}>
                <Form layout="vertical">
                    {header_pred}
                    {field_feedback}
                </Form>
            </Modal>);
        }
    }
);


class PageFormImage extends Component {


    constructor(props) {
        super(props);
        this.state = {
            visible: false,
            choice_obj: null,
            obj_name: null,
            prediction: null,
            success_prediction: null
        };

        this.upload_props = {
            name: 'image',
            accept: 'image/*',
            multiple: false,
            action: 'http://0.0.0.0:8000/api/ocr/',
            headers: {
                authorization: 'authorization-text',
            },
            onChange: this.onUploadImage,
        };

        this.handleChoiceSuccessPredChange = this.handleChoiceSuccessPredChange.bind(this);
    }


    handleChoiceSuccessPredChange(success_pred) {
        this.setState({
            success_prediction: success_pred
        });
    }

    onUploadImage = (info) => {
        if (info.file.status === 'done') {
            if (info.file.response['predictions'].length > 0) {
                this.setState({
                    visible: true,
                    prediction: info.file.response,
                    success_prediction: null
                });
            } else if (info.file.status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
            }
        }
    };

    handleOk = () => {
        const form = this.formRef.props.form;
        form.validateFields((err, values) => {
            if (err) {
                return;
            }
            let prediction = this.state.prediction;
            if(values['success_prediction'] === 1){
                console.log("ENTRO!! " , prediction.predictions[0].label);
                prediction['label'] = prediction.predictions[0].label;
            }else {
                if(values['choice_obj'] < prediction.predictions.length){
                    prediction['label'] = prediction.predictions[values['choice_obj']].label;
                }else{
                    prediction['label'] = values['text_obj'];
                }
            }
            let body = JSON.stringify(prediction);
            fetch(`http://0.0.0.0:8000/api/ocr/${prediction.id}/`, {method: "PUT", body,
                headers: {"Content-Type": "application/json"}})
                .then(res => res.json())
                .then(pred => {
                    message.success(`Su respuesta ah sido guardada, gracias por ayudarnos`);
                    form.resetFields();
                    this.setState({ visible: false });
                });
        });
    };


    handleCancel = (e) => {
        const form = this.formRef.props.form;
        form.resetFields();
        this.setState({
            visible: false,
        });
    };

    saveFormRef = (formRef) => {
        this.formRef = formRef;
    };

    render() {

        return (
            <div>
                <PredictionForm
                    wrappedComponentRef={this.saveFormRef}
                    visible={this.state.visible}
                    prediction={this.state.prediction}
                    onCancel={this.handleCancel}
                    onCreate={this.handleOk}
                    handleChoiceSuccessPredChange={this.handleChoiceSuccessPredChange}
                    success_prediction={this.state.success_prediction}
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
