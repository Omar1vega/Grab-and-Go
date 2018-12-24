package com.amazotgo.storeapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;

import com.amazotgo.storeapp.dummy.DummyContent;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;

import static com.amazotgo.storeapp.GoogleSignInActivity.googleSignInOptions;

public class Main2Activity extends AppCompatActivity implements TransactionFragment.OnListFragmentInteractionListener {

    private final static Fragment transactions = new TransactionFragment();
    private final static Fragment store = new StoreFragment();
    private final static Fragment account = new AccountFragment();
    private final FragmentManager fragmentManager = getSupportFragmentManager();
    private Fragment activeFragment = store;

    private FirebaseAuth mAuth;
    private GoogleSignInClient mGoogleSignInClient;


    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener = new BottomNavigationView.OnNavigationItemSelectedListener() {
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_transactions:
                    fragmentManager.beginTransaction().hide(activeFragment).show(transactions).commit();
                    activeFragment = transactions;
                    return true;
                case R.id.navigation_store:
                    fragmentManager.beginTransaction().hide(activeFragment).show(store).commit();
                    activeFragment = store;
                    return true;
                case R.id.navigation_account:
                    fragmentManager.beginTransaction().hide(activeFragment).show(account).commit();
                    activeFragment = account;
                    return true;
            }
            return false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        mGoogleSignInClient = GoogleSignIn.getClient(this, googleSignInOptions);
        mAuth = FirebaseAuth.getInstance();

        BottomNavigationView navigation = findViewById(R.id.navigation);
        navigation.setSelectedItemId(R.id.navigation_store);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        fragmentManager.beginTransaction().add(R.id.container, store, "1").commit();
        fragmentManager.beginTransaction().add(R.id.container, transactions, "2").hide(transactions).commit();
        fragmentManager.beginTransaction().add(R.id.container, account, "3").hide(account).commit();
    }

    @Override
    public void onListFragmentInteraction(DummyContent.DummyItem item) {

    }

    @Override
    public void onPointerCaptureChanged(boolean hasCapture) {

    }

    void signOut() {
        // Firebase sign out
        mAuth.signOut();

        // Google sign out
        mGoogleSignInClient.signOut().addOnCompleteListener(this,
                new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        startActivity(new Intent(Main2Activity.this, GoogleSignInActivity.class));
                        finish();
                    }
                });
    }

    FirebaseAuth getAuth() {
        return mAuth;
    }
}
