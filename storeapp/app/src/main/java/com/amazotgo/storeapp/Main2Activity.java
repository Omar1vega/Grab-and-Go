package com.amazotgo.storeapp;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;

import com.amazotgo.storeapp.dummy.DummyContent;

public class Main2Activity extends AppCompatActivity implements TransactionFragment.OnListFragmentInteractionListener {

    private final static Fragment transactions = new TransactionFragment();
    private final static Fragment store = new StoreFragment();
    private final static Fragment account = new AccountFragment();
    private final FragmentManager fragmentManager = getSupportFragmentManager();

    private Fragment activeFragment = store;

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
}
