#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, torch, logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

# ===================== Configuration =====================
MODEL_PATH = "fixhr_model"
BASE_MODEL = "tiiuae/falcon-7b-instruct"
MAX_LENGTH = 512
# ========================================================

logger = logging.getLogger(__name__)

class FixHRModelInference:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loaded = False
        
    def load_model(self):
        """Load the trained model and tokenizer"""
        try:
            if not os.path.exists(MODEL_PATH):
                logger.error(f"Model path not found: {MODEL_PATH}")
                return False
                
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            # Load base model
            base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL,
                dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True,
            )
            
            # Load fine-tuned model
            self.model = PeftModel.from_pretrained(base_model, MODEL_PATH)
            self.model.eval()
            
            self.is_loaded = True
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def generate_response(self, user_input, max_new_tokens=200):
        """Generate response using the trained model"""
        if not self.is_loaded:
            if not self.load_model():
                return "Model not available. Please train the model first."
        
        try:
            # Format input
            prompt = f"<s>[INST] {user_input} [/INST]"
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=MAX_LENGTH,
                padding=True
            ).to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part
            if "[/INST]" in response:
                response = response.split("[/INST]")[-1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"
    
    def extract_command(self, user_input):
        """Extract command from user input using the model"""
        response = self.generate_response(user_input)
        
        # Parse the response to extract commands
        commands = self.parse_commands(response)
        return {
            "original_input": user_input,
            "model_response": response,
            "extracted_commands": commands,
            "command_type": self.classify_command(commands)
        }
    
    def parse_commands(self, response):
        """Parse commands from model response"""
        commands = []
        
        # Look for specific command patterns
        patterns = [
            r"apply leave for (.+?)(?:\n|$)",
            r"apply gatepass for (.+?)(?:\n|$)",
            r"apply missed punch for (.+?)(?:\n|$)",
            r"my leave balance",
            r"my leaves?",
            r"pending leave",
            r"pending gatepass",
            r"my missed punch",
            r"today holiday",
            r"tomorrow holiday",
            r"next holiday",
            r"previous holiday",
            r"holiday list for (.+?)(?:\n|$)",
            r"attendance report for (.+?)(?:\n|$)",
            r"absent report for (.+?)(?:\n|$)",
            r"late report for (.+?)(?:\n|$)",
            r"approve leave\|(.+?)(?:\n|$)",
            r"reject leave\|(.+?)(?:\n|$)",
            r"approve gatepass\|(.+?)(?:\n|$)",
            r"reject gatepass\|(.+?)(?:\n|$)",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, str):
                    commands.append(match.strip())
                else:
                    commands.extend([m.strip() for m in match if m.strip()])
        
        # If no specific commands found, return the full response
        if not commands:
            commands = [response.strip()]
            
        return commands
    
    def classify_command(self, commands):
        """Classify the type of command"""
        if not commands:
            return "unknown"
            
        command_text = " ".join(commands).lower()
        
        if any(keyword in command_text for keyword in ["apply leave", "leave for"]):
            return "apply_leave"
        elif any(keyword in command_text for keyword in ["apply gatepass", "gatepass for"]):
            return "apply_gatepass"
        elif any(keyword in command_text for keyword in ["apply missed punch", "missed punch for"]):
            return "apply_missed_punch"
        elif any(keyword in command_text for keyword in ["leave balance", "my balance"]):
            return "leave_balance"
        elif any(keyword in command_text for keyword in ["my leaves", "my leave"]):
            return "my_leaves"
        elif any(keyword in command_text for keyword in ["pending leave"]):
            return "pending_leaves"
        elif any(keyword in command_text for keyword in ["pending gatepass"]):
            return "pending_gatepass"
        elif any(keyword in command_text for keyword in ["my missed punch", "my missed"]):
            return "my_missed_punch"
        elif any(keyword in command_text for keyword in ["holiday", "chhutti"]):
            return "holiday"
        elif any(keyword in command_text for keyword in ["attendance", "report"]):
            return "attendance"
        elif any(keyword in command_text for keyword in ["approve", "reject"]):
            return "approval"
        else:
            return "general"

# Global instance
model_inference = FixHRModelInference()

def get_model_response(user_input):
    """Get model response for user input"""
    return model_inference.extract_command(user_input)

def is_model_available():
    """Check if model is available"""
    return model_inference.is_loaded or os.path.exists(MODEL_PATH)
