package com.amazotgo.storeapp;


import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

public class AccountFragment extends Fragment {
    private Button signOutButton;
    private Main2Activity main;
    private TextView authenticatedUser;

    public AccountFragment() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_account, container, false);
        main = (Main2Activity) getActivity();

        signOutButton = view.findViewById(R.id.signOutButton);
        signOutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                main.signOut();
            }
        });

        authenticatedUser = view.findViewById(R.id.auth_user_name);
        if (main.getAuth().getCurrentUser().getDisplayName() != null) {
            authenticatedUser.setText(main.getAuth().getCurrentUser().getDisplayName());
        }
        return view;
    }
}
