package com.amazotgo.storeapp;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
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

public class MainActivity extends AppCompatActivity {
    public final String TAG = this.getClass().getCanonicalName();
    private Animation blink;
    private DatabaseReference mDatabase;
    private DatabaseReference mDistanceReference;
    private TextView distanceContainer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTitle(R.string.app_name);
        setContentView(R.layout.activity_main);

        mDatabase = FirebaseDatabase.getInstance().getReference();
        mDistanceReference = mDatabase.child("distance");
        distanceContainer = findViewById(R.id.distance_container);
        blink = AnimationUtils.loadAnimation(this, R.anim.blink);
    }

    @Override
    public void onStart() {
        super.onStart();

        ValueEventListener distanceListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                Distance distance = dataSnapshot.getValue(Distance.class);
                if (distance != null) {
                    distanceContainer.clearAnimation();
                    distanceContainer.setText(String.format("%s cm", String.valueOf(distance.distance)));
                    distanceContainer.startAnimation(blink);
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Log.w(TAG, "onCancelled", databaseError.toException());
                Toast.makeText(MainActivity.this, "Failed to load distance.",
                        Toast.LENGTH_SHORT).show();
            }
        };
        mDistanceReference.addValueEventListener(distanceListener);
    }
}
