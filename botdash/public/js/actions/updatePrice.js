/**
 * Copyright 2015, Cory Pruce
 *
 */
'use strict';
var PriceStore = require('../stores/PriceStore');

module.exports = function (context, payload, done) {
    var priceStore = context.getStore(PriceStore);

    var num = random(0, 81);
    var date = 1447797126637;      

    var newData = priceStore.createUpdate({
        date: date,
        num: num
    });
    
    context.dispatch('CREATE_PRICE_UPDATE', [newData]);
    context.service.create('new data', newData, {}, function (err) {
        if (err) {
            context.dispatch('CREATE_PRICE_UPDATE_FAILURE', [newData]);
            done();
            return;
        }
        context.dispatch('CREATE_PRICE_UPDATE_SUCCESS', [message]);
        done();
    });
};
