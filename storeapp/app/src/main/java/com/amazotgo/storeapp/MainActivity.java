package com.amazotgo.storeapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.amazotgo.storeapp.models.Distance;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import static com.amazotgo.storeapp.GoogleSignInActivity.googleSignInOptions;

public class MainActivity extends AppCompatActivity {
    public final String TAG = this.getClass().getCanonicalName();
    private Animation blink;
    private DatabaseReference mDatabase;
    private DatabaseReference mDistanceReference;
    private TextView distanceContainer;
    private Button signOutButton;

    private FirebaseAuth mAuth;
    private GoogleSignInClient mGoogleSignInClient;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTitle(R.string.app_name);
        setContentView(R.layout.activity_main);

        mDatabase = FirebaseDatabase.getInstance().getReference();
        mDistanceReference = mDatabase.child("distance");

        mGoogleSignInClient = GoogleSignIn.getClient(this, googleSignInOptions);
        mAuth = FirebaseAuth.getInstance();

        distanceContainer = findViewById(R.id.distance_container);
        signOutButton = findViewById(R.id.signOutButton);
        signOutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                signOut();
            }
        });
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


    private void signOut() {
        // Firebase sign out
        mAuth.signOut();

        // Google sign out
        mGoogleSignInClient.signOut().addOnCompleteListener(this,
                new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        startActivity(new Intent(MainActivity.this, GoogleSignInActivity.class));
                        finish();
                    }
                });
    }
}
