package com.amazotgo.storeapp.repositories;

import android.arch.lifecycle.MutableLiveData;

import com.amazotgo.storeapp.models.Item;

import java.util.ArrayList;
import java.util.List;


/**
 * Singleton pattern
 */
public class ItemRepository {

    private static ItemRepository instance;
    private ArrayList<Item> dataSet = new ArrayList<>();

    public static ItemRepository getInstance() {
        if (instance == null) {
            instance = new ItemRepository();
        }
        return instance;
    }


    // Pretend to get data from a webservice or online source
    public MutableLiveData<List<Item>> getItems() {
        MutableLiveData<List<Item>> data = new MutableLiveData<>();
        data.setValue(dataSet);
        return data;
    }
}












