package com.amazotgo.storeapp;

import android.arch.lifecycle.LiveData;
import android.arch.lifecycle.MutableLiveData;
import android.arch.lifecycle.ViewModel;

import com.amazotgo.storeapp.models.Item;
import com.amazotgo.storeapp.repositories.ItemRepository;

import java.util.List;

public class StoreFragmentViewModel extends ViewModel {
    private MutableLiveData<List<Item>> mNicePlaces;
    private MutableLiveData<Boolean> mIsUpdating = new MutableLiveData<>();

    void init() {
        if (mNicePlaces != null) {
            return;
        }
        ItemRepository mRepo = ItemRepository.getInstance();
        mNicePlaces = mRepo.getItems();
    }

    void addNewValue(final Item nicePlace) {
        List<Item> currentItems = mNicePlaces.getValue();
        if (currentItems != null && !currentItems.contains(nicePlace)) {
            currentItems.add(nicePlace);
        }
        mIsUpdating.setValue(true);
        mNicePlaces.postValue(currentItems);

    }

    LiveData<List<Item>> getNicePlaces() {
        return mNicePlaces;
    }


    public LiveData<Boolean> getIsUpdating() {
        return mIsUpdating;
    }
}
