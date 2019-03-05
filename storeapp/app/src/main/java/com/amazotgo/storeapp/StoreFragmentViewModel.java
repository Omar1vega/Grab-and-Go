package com.amazotgo.storeapp;

import android.arch.lifecycle.LiveData;
import android.arch.lifecycle.MutableLiveData;
import android.arch.lifecycle.ViewModel;

import com.amazotgo.storeapp.models.Item;
import com.amazotgo.storeapp.repositories.ItemRepository;

import java.util.List;

public class StoreFragmentViewModel extends ViewModel {
    public StoreFragmentViewModel() {
    }

    private MutableLiveData<List<Item>> items;

    void init() {
        if (items != null) {
            return;
        }
        ItemRepository mRepo = ItemRepository.getInstance();
        items = mRepo.getItems();
    }

    void clearItems() {
        List<Item> currentItems = items.getValue();
        if (currentItems != null) {
            currentItems.clear();
            items.postValue(currentItems);
        }
    }

    LiveData<List<Item>> getItems() {
        return items;
    }

    void setItems(List<Item> itemList) {
        clearItems();
        List<Item> currentItems = items.getValue();
        if (currentItems != null) {
            currentItems.addAll(itemList);
            items.postValue(currentItems);
        }

    }
}
