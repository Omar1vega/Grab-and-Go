package com.amazotgo.storeapp;


import android.arch.lifecycle.Observer;
import android.arch.lifecycle.ViewModelProviders;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.Toast;

import com.amazotgo.storeapp.adapters.RecyclerAdapter;
import com.amazotgo.storeapp.models.Item;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class StoreFragment extends Fragment {
    public final String TAG = this.getClass().getCanonicalName();

    private StoreFragmentViewModel storeFragmentViewModel;

    private MainActivity main;
    private DatabaseReference cartReference;

    private RecyclerView mRecyclerView;
    private RecyclerAdapter mAdapter;
    private ImageView emptyCartImage;


    public StoreFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_store, container, false);
        main = (MainActivity) getActivity();

        DatabaseReference mDatabase = FirebaseDatabase.getInstance().getReference();

        String userId = main.getAuth().getCurrentUser().getUid();
        cartReference = mDatabase.child("carts/" + userId + "/items");

        mRecyclerView = view.findViewById(R.id.item_list);
        emptyCartImage = view.findViewById(R.id.cart_empty_image);

        storeFragmentViewModel = ViewModelProviders.of(this).get(StoreFragmentViewModel.class);
        storeFragmentViewModel.init();
        storeFragmentViewModel.getItems().observe(this, new Observer<List<Item>>() {
            @Override
            public void onChanged(@Nullable List<Item> items) {
                mAdapter.notifyDataSetChanged();
                if (mAdapter.getItemCount() > 0) {
                    emptyCartImage.setVisibility(View.GONE);
                } else {
                    emptyCartImage.setVisibility(View.VISIBLE);
                }
            }
        });

        initRecyclerView();
        return view;
    }

    @Override
    public void onStart() {
        super.onStart();
        cartReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                storeFragmentViewModel.clearItems();
                List<Item> items = new ArrayList<>();
                boolean itemsChanged = false;
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    if (snapshot.getValue() != null && !snapshot.getValue().equals("")) {
                        itemsChanged = true;
                        Item item = snapshot.getValue(Item.class);
                        items.add(item);
                    }
                }
                if (itemsChanged) {
                    storeFragmentViewModel.setItems(items);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                Log.w(TAG, "onCancelled", databaseError.toException());
                Toast.makeText(main, "Failed to load items from cart.", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void initRecyclerView() {
        mAdapter = new RecyclerAdapter(this.getContext(), storeFragmentViewModel.getItems().getValue());
        RecyclerView.LayoutManager linearLayoutManager = new LinearLayoutManager(this.getContext());
        mRecyclerView.setLayoutManager(linearLayoutManager);
        mRecyclerView.setAdapter(mAdapter);
        if (mAdapter.getItemCount() == 0) {
            emptyCartImage.setVisibility(View.VISIBLE);
        }
    }
}
