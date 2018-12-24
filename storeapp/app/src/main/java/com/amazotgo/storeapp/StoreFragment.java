package com.amazotgo.storeapp;


import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.TextView;
import android.widget.Toast;

import com.amazotgo.storeapp.models.Distance;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class StoreFragment extends Fragment {
    public final String TAG = this.getClass().getCanonicalName();
    private Main2Activity main;
    private DatabaseReference mDatabase;
    private DatabaseReference mDistanceReference;

    private TextView distanceContainer;
    private Animation blink;


    public StoreFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_store, container, false);
        main = (Main2Activity) getActivity();

        mDatabase = FirebaseDatabase.getInstance().getReference();
        mDistanceReference = mDatabase.child("distance");

        distanceContainer = view.findViewById(R.id.distance_container);
        blink = AnimationUtils.loadAnimation(main, R.anim.blink);
        return view;
    }

    @Override
    public void onStart() {
        super.onStart();

        mDistanceReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Distance distance = dataSnapshot.getValue(Distance.class);
                if (distance != null) {
                    distanceContainer.clearAnimation();
                    distanceContainer.setText(String.format("%s cm", String.valueOf(distance.distance)));
                    distanceContainer.startAnimation(blink);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                Log.w(TAG, "onCancelled", databaseError.toException());
                Toast.makeText(main, "Failed to load distance.", Toast.LENGTH_SHORT).show();
            }
        });

    }
}
