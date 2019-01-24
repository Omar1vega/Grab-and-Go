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
    public MutableLiveData<List<Item>> getNicePlaces() {
        setNicePlaces();
        MutableLiveData<List<Item>> data = new MutableLiveData<>();
        data.setValue(dataSet);
        return data;
    }

    private void setNicePlaces() {
        dataSet.add(
                new Item("https://c1.staticflickr.com/5/4636/25316407448_de5fbf183d_o.jpg",
                        "Havasu Falls")
        );
        dataSet.add(
                new Item("https://i.redd.it/tpsnoz5bzo501.jpg",
                        "Trondheim")
        );
        dataSet.add(
                new Item("https://i.redd.it/qn7f9oqu7o501.jpg",
                        "Portugal")
        );
        dataSet.add(
                new Item("https://i.redd.it/j6myfqglup501.jpg",
                        "Rocky Mountain National Park")
        );
        dataSet.add(
                new Item("https://i.redd.it/0h2gm1ix6p501.jpg",
                        "Havasu Falls")
        );
        dataSet.add(
                new Item("https://i.redd.it/k98uzl68eh501.jpg",
                        "Mahahual")
        );
        dataSet.add(
                new Item("https://c1.staticflickr.com/5/4636/25316407448_de5fbf183d_o.jpg",
                        "Frozen Lake")
        );
        dataSet.add(
                new Item("https://i.redd.it/obx4zydshg601.jpg",
                        "Austrailia")
        );
    }
}












