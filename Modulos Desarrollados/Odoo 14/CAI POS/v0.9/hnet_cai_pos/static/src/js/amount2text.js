/*
    @author ebenedetto@hnetw.com - HNET
    @date 28/07/2021
    @decription Convertir el total de la factura en texto
    @name_file amount2text.js
    @version 1.0
*/

odoo.define('pos_amount_to_text.amount2text', function (require) {
"use strict";

var pos_model_order = require('point_of_sale.models');


var PosOrderSuper = pos_model_order.Order.prototype;

pos_model_order.Order = pos_model_order.Order.extend({
    initialize: function(attributes, options) {
    	this.sequence_order = null;
        return PosOrderSuper.initialize.call(this,attributes,options);
    },	

	amount_text: function () { // PARA ESPAÑOL
        var number_in = this.get_total_with_tax();   
        //console.log(number_in);           
        var converted = '' ;                            
        if (typeof(number_in) != 'string') {
            var number = number_in.toFixed(2);
            //console.log(number);
        }
        else{                       
          var number = number_in;
        }
        var number_str = number ;                                    
        var lista = number_str.split("."); //comprobamos si tiene decimal            
        if (lista.length>1) {
            var number_int = lista[0]; // parte entera
            var number_dec = lista[1]; // parte decimal
        } 
        else {
            number_int = number_str;                              
            number_dec = "";
        }

        number_str = ('000000000' + number_int).slice(-9); // copletamos con 0 a la izquierda

        var millones = number_str.substring(0,3); // extrae las tres primeros caracteres de la izquierda      
        //console.log("ERROR1", millones );
        var miles = number_str.substring(3,6);       
        var cientos = number_str.substring(6);

        if (parseInt(millones)>0) {
            if (millones == '001') {
                converted += 'UN MILLON ';
            }
            else if (parseInt(millones) > 0) {    
                converted +=  this.convertNumber(millones) + 'MILLONES ';
            }
        }

        if (parseInt(miles)>0) {                                                    
            if (miles == '001') {                                       
                converted += 'MIL ';
                }                                 
            else if (parseInt(miles) > 0) {
                converted += this.convertNumber(miles) + 'MIL ' ;
            }
        } 

        if (parseInt(cientos)>0) {                                                  
            if (cientos == '001') {                                     
                converted += 'UN ';
            }                                   
            else if (parseInt(cientos) > 0) {                                   
                converted += this.convertNumber(cientos) + ' ' ;
            }
        }

        if (number_dec == "") {
            number_dec = "00";
        }

        if (number_dec.length < 2 ){
          number_dec+='0';
        }


        if(number_dec == '00'){
            converted += 'LEMPIRAS CON CERO CENTAVOS';
        }else{
            converted += 'LEMPIRAS CON '  + this.convertNumber(number_dec) +  ' CENTAVOS';
        }

        return converted ; 
        },
        
    convertNumber: function (n){
        var UNIDADES = ['','UNO ','DOS ','TRES ','CUATRO ','CINCO ','SEIS ','SIETE ','OCHO ','NUEVE ','DIEZ ', 'ONCE ','DOCE ','TRECE ','CATORCE ','QUINCE ','DIECISEIS ','DIECISIETE ','DIECIOCHO ','DIECINUEVE ','VEINTE '];
        var DECENAS = ['VEINTI','TREINTA ','CUARENTA ','CINCUENTA ','SESENTA ','SETENTA ','OCHENTA ','NOVENTA '];
        var CENTENAS = ['CIENTO ','DOSCIENTOS ','TRESCIENTOS ','CUATROCIENTOS ', 'QUINIENTOS ','SEISCIENTOS ','SETECIENTOS ','OCHOCIENTOS ','NOVECIENTOS '];
        var output = '';

        if(n == '100'){
            output = "CIEN ";
        }else{
            if (n[0] != '0') {
                if(n.toString().length > 2){
                    output = CENTENAS[parseInt(n[0])-1];
                }else{
                    if (n > 20){
                        output = DECENAS[parseInt(n[0])-2];
                    }else{
                        output = UNIDADES[parseInt(n)];
                    }
                }
            }
        }
        var k = parseInt(n.substring(1));
        if (k.toString().length > 1){
            if (k <= 20 ) {
                output +=  UNIDADES[k];
            }else {
                if((k > 30) & (n[2] != '0')){
                    //output += '%sY %s' % (DECENAS[parseInt(n[1])-2], UNIDADES[parseInt(n[2])]);
                    output += DECENAS[parseInt(n[1])-2] + 'Y ' + UNIDADES[parseInt(n[2])];
                }else{
                    //output += '%s%s' % (DECENAS[parseInt(n[1])-2], UNIDADES[parseInt(n[2])]);
                    output += DECENAS[parseInt(n[1])-2]  + UNIDADES[parseInt(n[2])];
                }
            }
        }else{
            if(((Array.from(output)).join('')).toString() == 'VEINTI'){
                output +=  UNIDADES[k];
            }else if((DECENAS.includes(output)) & n[1] != '0'){
                output += ' Y '+ UNIDADES[k];
            }else{
                output +=  UNIDADES[k];
            }
        }
        return output;
    },
});

});
