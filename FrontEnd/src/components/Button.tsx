import React from 'react';
import './Button.css';


interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
children: React.ReactNode;
}

export function Button({children, ...props}: ButtonProps) {
    return(
        <button className="custom-button" {...props}>
            {children}
        </button>
    );
}